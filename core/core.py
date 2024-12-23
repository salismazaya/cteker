from abc import ABC, abstractmethod
from helpers.decorators import cache_redis
from decimal import Decimal
from typing import Self
from helpers.limitter import RedisTransactionLimitter
from helpers.log import logger
import aiohttp

class Core(ABC):
    @abstractmethod
    def get_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_private_key(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def is_valid_address(self, address: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_address(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_client(self):
        raise NotImplementedError

    @abstractmethod
    def get_symbol(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_binance_ticker(self) -> str:
        raise NotImplementedError
    
    def as_redis_transaction_limitter(self, key: str, total_transactions: int, seconds: int, interval_sleep: float = 0.3) -> Self:
        return RedisTransactionLimitter(self, key, total_transactions, seconds, interval_sleep)

    @cache_redis(30)
    async def get_price(self) -> Decimal:
        ticker_binance = self.get_binance_ticker()
        url = f"https://data-api.binance.vision/api/v3/ticker/price?symbol={ticker_binance}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json()
                logger.debug("(%s) response from binance api: %s", ticker_binance, result)

        price = Decimal(result['price'])
        return price

    @abstractmethod
    async def get_balance(self) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    async def transfer(self, receipent: str, amount: float, *args, **kwargs) -> str:
        raise NotImplementedError

    def add_explorer(self, tx_hash: str):
        return tx_hash