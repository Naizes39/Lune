import redis.asyncio as redis
import asyncio
import hashlib

async def set_cache(prompt: str, response: str, ttl_seconds: int = 600) -> None:
    key = hashlib.md5(prompt.encode('utf-8')).hexdigest()
    r = redis.Redis(host='localhost', port=6380, decode_responses=True, password='lunecache')
    await r.set(key, response, ex=ttl_seconds)



async def get_cache(prompt: str) -> str | None:
    key = hashlib.md5(prompt.encode('utf-8')).hexdigest()
    r = redis.Redis(host='localhost', port=6380, decode_responses=True, password='lunecache')
    return await r.get(key)


