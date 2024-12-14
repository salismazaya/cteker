from core.core import Core
from abc import abstractmethod
from web3.middleware.geth_poa import async_geth_poa_middleware
from web3 import AsyncWeb3, Account
from core import constants
from helpers.redis import redis_client
from helpers.decorators import cache_redis
import re, asyncio
import exceptions.transaction

transaction_lock = asyncio.Lock() 

class EvmCore(Core):
    def __init__(self):
        super().__init__()
        self._chain_id = None
        self._w3 = self.get_client()

    @property
    def w3(self):
        return self._w3

    @abstractmethod
    def get_http_rpc(self) -> str:
        raise NotImplementedError("rpc not implemented")
    
    async def get_chain_id(self) -> int:
        if self._chain_id is None:
            self._chain_id = await self.w3.eth.chain_id
        
        return self._chain_id

    # def get_http_rpc_for_price_contract(self):
    #     return self.get_http_rpc()

    async def get_current_nonce(self):
        return int(await self.w3.eth.get_transaction_count(self.get_address(), 'latest'))

    # def get_price_contract_address(self):
    #     raise NotImplementedError("price contract not implemnted")
    
    # def get_price_contract(self): 
    #     w3 = self.get_client(url = self.get_http_rpc_for_price_contract())
    #     return w3.eth.contract(
    #         w3.to_checksum_address(self.get_price_contract_address()),
    #         abi = constants.EVM_AGGREGATOR_CONTRACT_ABI
    #     )
    
    # async def get_price(self):
    #     # contract = self.get_price_contract()

    #     # # id_redis = f'get_price_{contract.address}'
    #     # # data_redis = await r.get(id_redis)

    #     # # if data_redis:
    #     # #     return int(data_redis)

    #     # amount = await contract.functions.latestAnswer().call()
    #     # decimals = await contract.functions.decimals().call()

    #     # amount /= (10 ** decimals)
    #     # return amount

    def get_client(self, url = None) -> AsyncWeb3:
        if url is None:
            url = self.get_http_rpc()

        w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(url))
        w3.middleware_onion.inject(async_geth_poa_middleware, layer = 0)
        return w3
    
    def is_valid_address(self, address: str) -> bool:
        eth_address_pattern = re.compile(r'^(0x)?[0-9a-fA-F]{40}$')
        return not eth_address_pattern.match(address) is None

    def get_private_key(self) -> str:
        return constants.EVM_PRIVATE_KEY

    def get_address(self) -> str:
        address = Account.from_key(self.get_private_key()).address
        return str(address)

    async def get_balance(self) -> float:
        address = Account.from_key(self.get_private_key()).address
        balance_wei = await self.w3.eth.get_balance(self.w3.to_checksum_address(address))
        return self.w3.from_wei(
            balance_wei,
            'ether'
        )
    
    async def get_nonce(self, address = None):
        chain_id = await self.get_chain_id()
        async with transaction_lock:
            nonce = int(await redis_client.get(f'nonce_evm_{chain_id}:{address}') or 0)
            if nonce < 0:
                nonce = await self.get_current_nonce()
                await redis_client.set(f'nonce_evm_{chain_id}:{address}', nonce)

        return nonce
    
    @cache_redis(120)
    async def get_gas_price(self):
        return await self.w3.eth.gas_price

    async def generate_trx(self, receipent: str, amount: float, gas = 21_000):
        sender_address = self.get_address()
        nonce = await self.get_nonce(sender_address)
        gas_price = await self.w3.eth.gas_price
        amount_wei = self.w3.to_wei(amount, 'ether')

        transaction = {
            'to': self.w3.to_checksum_address(receipent),
            'value': amount_wei,
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
            'chainId': await self.w3.eth.chain_id,
        }
        return transaction

    async def transfer(self, receipent: str, amount: float, gas: int = 2100) -> str:
        try:
            transaction = await self.generate_trx(receipent, amount, gas)
            signed_transaction = self.w3.eth.account.sign_transaction(transaction, self.get_private_key())
            tx_hash = await self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
            tx_hash_hex = tx_hash.hex()

            chain_id = await self.get_chain_id()
            address = self.get_address()

            async with transaction_lock:
                await redis_client.incr(f'nonce_evm_{chain_id}:{address}')

            return tx_hash_hex
        
        except ValueError as e:
            error_message = re.search(r"message': *'(.+)'\}", str(e))[1]
            raise exceptions.transaction.TransactionFailed(error_message)


class EvmTokenCore(EvmCore):
    def __init__(self):
        super().__init__()
        self.contract = self.w3.eth.contract(self.w3.to_checksum_address(self.get_token_address()), abi = constants.EVM_ERC20_CONTRACT_ABI)

    @abstractmethod
    def get_token_address(self) -> str:
        raise NotImplementedError

    async def get_decimals(self) -> int:
        chain_id = await self.get_chain_id()
        token_address = self.get_token_address()
        key = f'{chain_id}:{token_address}'
        decimals = await redis_client.get(f'decimals_{key}')
        if decimals is None:
            decimals = await self.contract.functions.decimals().call()
            decimals = await redis_client.set(f'decimals_{key}', decimals)
            return decimals

        return int(decimals.decode())

    async def get_balance(self) -> float:
        address = self.get_address()
        decimals = await self.get_decimals()
        balance = await self.contract.functions.balanceOf(address).call()
        return balance / (10 ** decimals)

    async def generate_trx(self, receipent: str, amount: float, gas = 70_000):
        address = self.get_address()
        nonce = await self.get_nonce(address)
        decimals = await self.get_decimals()
        amount = amount * (10 ** decimals)

        tx = await self.contract.functions.transfer(
            self.w3.to_checksum_address(receipent),
            amount
        ).build_transaction({
            'nonce': nonce,
            'gas': gas,
            'from': address,
            'chainId': await self.w3.eth.chain_id,
        })
        return tx
    