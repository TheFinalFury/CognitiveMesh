from typing import Any, Dict, Optional
from config.settings import settings
from src.adaptive_engine.telemetry import telemetry_tracker
from src.storage_connectors.redis_connector import redis_connector

class AdaptivePolicyManager:
    """Manages adaptive sharding, dynamic caching, and hotspot routing."""

    def __init__(self):
        self.telemetry = telemetry_tracker
        self.redis = redis_connector
        self.threshold = settings.CACHE_HOT_THRESHOLD

    def should_promote_to_hot_cache(self, entity_id: str) -> bool:
        """Determines if access frequency warrants dynamic promotion to Key-Value hot cache."""
        hits = self.telemetry.get_hit_count(entity_id)
        return hits >= self.threshold

    def promote_entity(self, entity_id: str, data: Dict[str, Any]) -> bool:
        """Dynamically caches entity into Redis hot storage."""
        cache_key = f"hot_cache:{entity_id}"
        return self.redis.set_json(cache_key, data, ttl=settings.CACHE_TTL_SECONDS)

    def check_hot_cache(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Attempts retrieval from the adaptive in-memory layer."""
        cache_key = f"hot_cache:{entity_id}"
        return self.redis.get_json(cache_key)

adaptive_policy = AdaptivePolicyManager()
