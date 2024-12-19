from helpers.redis import redis_client

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
