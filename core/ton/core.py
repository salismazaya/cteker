from core.core import Core
from abc import abstractmethod
from core import constants
from tonutils.wallet import WalletV4R2
from tonutils.client import TonapiClient
from tonutils.utils import Address
from tonutils.jetton import JettonMaster, JettonWallet
from tonutils.utils import to_amount
import aiohttp.client_exceptions
from helpers.locks import RedisLock
from decimal import Decimal
import asyncio, inspect

class TonMainnetClientMixin:
    def get_client(self):
        client = TonapiClient(api_key = constants.TONAPI_API_KEY)
        return client

    def get_address(self) -> str:
        return self.wallet.address.to_str(True, True, False, False)

class TonTestnetClientMixin:
    def get_client(self):
        client = TonapiClient(
            api_key = constants.TONAPI_API_KEY,
            is_testnet = True
        )
        return client
    
    def get_address(self) -> str:
        return self.wallet.address.to_str(True, True, False, True)
    
    
class TonCore(Core):
    def __init__(self):
        self._client = self.get_client()
        self._wallet = self.get_wallet()
        super().__init__()

    @property
    def client(self):
        return self._client
    
    @property
    def wallet(self):
        return self._wallet

    def get_private_key(self) -> str:
        return constants.TON_MNEMONIC

    def is_valid_address(self, address: str) -> bool:
        try:
            Address(address)
            return True
        except:
            return False

    @abstractmethod
    def get_client(self) -> TonapiClient:
        # client = ToncenterClient('', )
        # wallet, public_key, private_key, mnemonic = WalletV4R2.from_mnemonic(client, MNEMONIC)
        raise NotImplementedError

    def get_wallet(self) -> WalletV4R2:
        wallet, _, _, _ =  WalletV4R2.from_mnemonic(self.client, self.get_private_key())
        return wallet
    
    # def get_address(self) -> str:
    #     return self.client.address.to_str(True, True, False)
    
    async def get_balance(self) -> Decimal:
        try:
            balance = await self.wallet.get_balance(self.client, self.get_address())
            balance_without_decimals = balance / (10 ** 9)
            return Decimal(balance_without_decimals)
        except aiohttp.client_exceptions.ClientResponseError as e:
            if e.message == "entity not found":
                return Decimal(0)
            
            raise e
    
    def get_transaction_lock(self, receipent: str, amount: float) -> RedisLock:
        return RedisLock(f'{self.get_id()}:{receipent}:{amount}')

    async def transfer(self, receipent: str, amount: float, *args, **kwargs) -> str:
        async with self.get_transaction_lock(receipent, amount):
            tx_hash = await self.wallet.transfer(
                destination = receipent,
                amount = amount,
            )
            await asyncio.sleep(1)

        return tx_hash

class TonTokenCore(TonCore):
    @abstractmethod
    def get_token_address(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_decimals(self) -> int:
        raise NotImplementedError

    async def transfer(self, receipent: str, amount: float, *args, **kwargs) -> str:
        decimals = self.get_decimals()
        if inspect.isawaitable(decimals):
            decimals = await decimals
          
        async with self.get_transaction_lock(receipent, amount):
            tx_hash = await self.wallet.transfer_jetton(
                destination = receipent,
                jetton_master_address = self.get_token_address(),
                jetton_amount = amount,
                jetton_decimals = decimals
            )
            await asyncio.sleep(1)

        return tx_hash

    async def get_balance(self) -> Decimal:
        decimals = self.get_decimals()
        if inspect.iscoroutine(decimals):
            decimals = await decimals

        jetton_wallet_address = await JettonMaster.get_wallet_address(
            client = self.client,
            owner_address = self.get_address(),
            jetton_master_address = self.get_token_address(),
        )

        jetton_wallet_data = await JettonWallet.get_wallet_data(
            client = self.client,
            jetton_wallet_address = jetton_wallet_address,
        )

        return Decimal(
            to_amount(jetton_wallet_data.balance, decimals)
        )