from helpers.redis import redis_client
import asyncio

class DummyLock:
    async def __aenter__(self, *args, **kwargs):
        pass

    async def __aexit__(self, *args, **kwargs):
        pass

class RedisLockRateLimitter:
    def __init__(self, key: str, total_transactions: int, seconds: int, interval_sleep = 0.3):
        self._interval_sleep = interval_sleep 
        self._key = key
        self._total_transactions = total_transactions
        self._seconds = seconds

    @property
    def key(self):
        return f"lock_rate_limit_{self._key}"
    
    async def wait(self):
        while True:
            try:
                output = await redis_client.incr(self.key)
                await redis_client.expire(self.key, self._seconds, nx = True)
                if output <= self._total_transactions:
                    break
            finally:
                await asyncio.sleep(self._interval_sleep)

    async def __aenter__(self, *args, **kwargs):
        await self.wait()

    async def __aexit__(self, *args, **kwargs):
        pass


class RedisLock:
    def __init__(self, key: str, timeout: int = 120):
        self._key = key
        self._timeout = timeout
        self._lock = redis_client.lock(self.key, timeout = timeout)

    @property
    def key(self):
        return f"lock_{self._key}"

    async def __aenter__(self, *args, **kwargs):
        await self._lock.acquire()

    async def __aexit__(self, *args, **kwargs):
        await self._lock.release()
