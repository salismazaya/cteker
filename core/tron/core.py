from tronpy import AsyncTron
from tronpy.keys import PrivateKey, PublicKey
from tronpy.providers import AsyncHTTPProvider
from core.core import Core
from helpers.decorators import cache_redis
from core import constants
from abc import abstractmethod
from decimal import Decimal
import re

class TronMainnetClientMixin:
    def get_client(self):
        return AsyncTron(
            AsyncHTTPProvider(api_key = constants.TRON_GRID_API_KEY),
            network = "mainnet"
        )

class TronNileTestnetClientMixin:
    def get_client(self):
        return AsyncTron(
            network = "nile"
        )

class TronCore(Core):
    def get_private_key(self) -> str:
        return constants.TRON_PRIVATE_KEY

    def is_valid_address(self, address: str) -> bool:
        return bool(re.match(r'T[A-Za-z1-9]{33}', address))

    @abstractmethod
    def get_client(self) -> AsyncTron:
        pass

    def get_address(self) -> str:
        pub_key: PublicKey = PrivateKey.fromhex(self.get_private_key()).public_key
        address = pub_key.to_base58check_address()
        return address

    async def get_balance(self) -> Decimal:
        async with self.get_client() as client:
            pub_key: PublicKey = PrivateKey.fromhex(self.get_private_key()).public_key
            address = pub_key.to_base58check_address()
            
            try:
                return Decimal(await client.get_account_balance(address))
            except:
                return Decimal(0)
    
    async def execute_transfer(self, receipent: str, amount: float, gas = 1_000_000) -> str:
        async with self.get_client() as client:
            address = self.get_address()
            txb = client.trx.transfer(
                address,
                receipent,
                int(amount * 1_000_000)
            ).fee_limit(gas)
            txn = await txb.build()
            txn_ret = await txn.sign(PrivateKey.fromhex(self.get_private_key())).broadcast()
            rv = (await txn_ret.wait())['id']

            return rv

class TronTokenCore(TronCore):
    @abstractmethod
    def get_token_address(self):
        raise NotImplementedError
    
    @cache_redis(3600 * 24)
    async def get_decimals(self):
        async with self.get_client() as client:
            token_address = self.get_token_address()
            contract = await client.get_contract(token_address)
            return await contract.functions.decimals()

    async def execute_transfer(self, receipent: str, amount: float, gas = 10_000_000) -> str:
        async with self.get_client() as client:
            token_address = self.get_token_address()
            contract = await client.get_contract(token_address)
            address = self.get_address()
            decimals = await self.get_decimals()
            amount_with_decimals = int(amount * (10 ** decimals))
            txb = await contract.functions.transfer(
                receipent,
                amount_with_decimals
            )
            txb = txb.with_owner(address).fee_limit(gas)
            txn = await txb.build()
            txn_ret = await txn.sign(PrivateKey.fromhex(self.get_private_key())).broadcast()
            rv = (await txn_ret.wait())['id']

            return rv

    async def get_balance(self) -> Decimal:
        async with self.get_client() as client:
            token_address = self.get_token_address()
            contract = await client.get_contract(token_address)
            address = self.get_address()
            result = await contract.functions.balanceOf(address) / (10 ** await self.get_decimals())
            return Decimal(result)