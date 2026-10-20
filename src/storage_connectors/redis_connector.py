import json
from typing import Any, Optional
import redis
from config.settings import settings
from src.storage_connectors.base import BaseStorageConnector

class RedisConnector(BaseStorageConnector):
    """Connector for Redis Key-Value and In-Memory Hot Cache."""

    def __init__(self):
        self.client: Optional[redis.Redis] = None

    def connect(self) -> None:
        if not self.client:
            self.client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD or None,
                decode_responses=True,
                socket_timeout=2.0
            )

    def ping(self) -> bool:
        try:
            if not self.client:
                self.connect()
            return bool(self.client.ping())
        except Exception:
            return False

    def get_json(self, key: str) -> Optional[Any]:
        if not self.client:
            self.connect()
        val = self.client.get(key)
        if val:
            try:
                return json.loads(val)
            except Exception:
                return val
        return None

    def set_json(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        if not self.client:
            self.connect()
        serialized = json.dumps(value)
        return bool(self.client.set(key, serialized, ex=ttl or settings.CACHE_TTL_SECONDS))

    def incr(self, key: str) -> int:
        if not self.client:
            self.connect()
        return self.client.incr(key)

    def close(self) -> None:
        if self.client:
            self.client.close()
            self.client = None

redis_connector = RedisConnector()
