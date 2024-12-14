from redis.asyncio import Redis
import os

def get_redis_client():
    redis_client = Redis.from_url(os.environ['REDIS_URL'])
    return redis_client

redis_client = get_redis_client()