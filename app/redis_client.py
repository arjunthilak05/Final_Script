import redis.asyncio as redis
from app.config import settings
from typing import Optional


class RedisClient:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
    
    async def initialize(self):
        """Initialize Redis connection (alias for connect)"""
        await self.connect()
    
    async def connect(self):
        """Connect to Redis"""
        self.redis = redis.from_url(settings.redis_url)
        await self.redis.ping()
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str):
        """Get value from Redis"""
        if self.redis:
            result = await self.redis.get(key)
            return result.decode('utf-8') if result else None
        return None
    
    async def set(self, key: str, value: str, expire: Optional[int] = None):
        """Set value in Redis"""
        if self.redis:
            return await self.redis.set(key, value, ex=expire)
        return False
    
    async def delete(self, key: str):
        """Delete key from Redis"""
        if self.redis:
            return await self.redis.delete(key)
        return False
    
    async def exists(self, key: str):
        """Check if key exists in Redis"""
        if self.redis:
            return await self.redis.exists(key)
        return False
    
    async def keys(self, pattern: str):
        """Get keys matching pattern from Redis"""
        if self.redis:
            keys = await self.redis.keys(pattern)
            return [key.decode('utf-8') if isinstance(key, bytes) else key for key in keys]
        return []


# Global Redis client instance
redis_client = RedisClient()
