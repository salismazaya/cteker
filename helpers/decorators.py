from functools import wraps
from helpers.redis import redis_client
import pickle

def cache_redis(expired: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            hashed_func_value = hash(func)
            hashed_args_value = hash(frozenset(args))
            hashed_kwargs_value = hash(frozenset(kwargs.items()))
            key = f"cache_redis_{hashed_func_value}:{hashed_args_value}:{hashed_kwargs_value}"
            cache_value = await redis_client.get(key)
            if cache_value is None:
                result = await func(*args, **kwargs)
                pickled_result = pickle.dumps(result)
                await redis_client.set(key, pickled_result, ex = expired)
                return result

            depickled_value = pickle.loads(cache_value) 
            return depickled_value
        
        return wrapper
    
    return decorator