import time
from collections import defaultdict
from typing import Dict, Any, List

class QueryTelemetryTracker:
    """Tracks query latency, access frequency, and entity hotspot statistics."""

    def __init__(self):
        self.access_counts: Dict[str, int] = defaultdict(int)
        self.latency_records: List[Dict[str, Any]] = []

    def record_access(self, entity_id: str, latency_ms: float, target_engine: str):
        self.access_counts[entity_id] += 1
        self.latency_records.append({
            "entity_id": entity_id,
            "target_engine": target_engine,
            "latency_ms": latency_ms,
            "timestamp": time.time()
        })
        # Keep last 1000 records
        if len(self.latency_records) > 1000:
            self.latency_records.pop(0)

    def get_hit_count(self, entity_id: str) -> int:
        return self.access_counts.get(entity_id, 0)

    def get_stats(self) -> Dict[str, Any]:
        total_queries = len(self.latency_records)
        avg_latency = (
            sum(r["latency_ms"] for r in self.latency_records) / total_queries
            if total_queries > 0 else 0.0
        )
        return {
            "total_recorded_queries": total_queries,
            "average_latency_ms": round(avg_latency, 2),
            "tracked_entities_count": len(self.access_counts),
            "top_hot_entities": sorted(self.access_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }

telemetry_tracker = QueryTelemetryTracker()
