import time
from typing import Any, Dict, List, Optional
from src.adaptive_engine.policy_manager import adaptive_policy
from src.adaptive_engine.telemetry import telemetry_tracker
from src.storage_connectors.mongo_connector import mongo_connector
from src.storage_connectors.neo4j_connector import neo4j_connector
from src.storage_connectors.redis_connector import redis_connector

class MeshQueryPlanner:
    """Orchestrates multi-model execution and transparent polyglot data retrieval."""

    def __init__(self):
        self.mongo = mongo_connector
        self.redis = redis_connector
        self.neo4j = neo4j_connector
        self.policy = adaptive_policy
        self.telemetry = telemetry_tracker

    def execute_entity_lookup(self, entity_id: str, collection: str = "products") -> Dict[str, Any]:
        """Resolves an entity across hot-cache, document store, and graph layers."""
        start_time = time.time()

        # Step 1: Check Adaptive Hot Cache (Redis)
        cached_data = self.policy.check_hot_cache(entity_id)
        if cached_data:
            latency = (time.time() - start_time) * 1000
            self.telemetry.record_access(entity_id, latency, target_engine="redis_hot_cache")
            cached_data["_mesh_source"] = "redis_hot_cache"
            cached_data["_latency_ms"] = round(latency, 2)
            return cached_data

        # Step 2: Fetch Primary Document from MongoDB
        doc = self.mongo.find_by_id(collection, entity_id) or {"id": entity_id}
        source_engine = "mongodb_document"

        # Step 3: Fetch Graph Relations from Neo4j (if available)
        try:
            cypher = "MATCH (e {id: $eid})-[r]-(target) RETURN type(r) AS relation, properties(target) AS connected_entity LIMIT 5"
            graph_relations = self.neo4j.execute_cypher(cypher, {"eid": entity_id})
            doc["_graph_connections"] = graph_relations
        except Exception:
            doc["_graph_connections"] = []

        latency = (time.time() - start_time) * 1000
        self.telemetry.record_access(entity_id, latency, target_engine=source_engine)

        # Step 4: Evaluate for Adaptive Hot Cache Promotion
        if self.policy.should_promote_to_hot_cache(entity_id):
            self.policy.promote_entity(entity_id, doc)
            doc["_mesh_promoted_to_cache"] = True

        doc["_mesh_source"] = source_engine
        doc["_latency_ms"] = round(latency, 2)
        return doc

mesh_planner = MeshQueryPlanner()
