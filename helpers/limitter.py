from helpers.locks import RedisLockRateLimitter
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Awaitable
    import core.core

@dataclass
class RedisTransactionLimitter:
    children: 'core.core.Core'
    key: str
    total_transactions: int
    seconds: int
    interval_sleep: float = 0.3

    def get_ratelimitter(self):
        return RedisLockRateLimitter(
            key = self.key,
            total_transactions = self.total_transactions,
            seconds = self.seconds,
            interval_sleep = self.interval_sleep
        )

    def __use_ratelimitter(self, callback: 'Awaitable'):
        async def wrapper(*args, **kwargs):
            async with self.get_ratelimitter():
                return await callback(*args, **kwargs)

        return wrapper
    
    def __getattr__(self, value: str):
        callback = getattr(self.children, value)
        if value == 'transfer':
            callback = self.__use_ratelimitter(callback)
        
        return callback