from typing import Any, Dict, List, Optional
from src.semantic_indexing.embedder import semantic_embedder
from src.storage_connectors.qdrant_connector import qdrant_connector

class UniversalSemanticRegistry:
    """Manages cross-engine entity linkages in the shared vector embedding space."""

    def __init__(self):
        self.connector = qdrant_connector
        self.embedder = semantic_embedder

    def index_entity(
        self,
        point_id: int,
        context_text: str,
        entity_id: str,
        mongo_collection: Optional[str] = None,
        redis_key: Optional[str] = None,
        neo4j_node_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Embeds contextual text and stores linkage pointers to physical NoSQL stores."""
        vector = self.embedder.embed_text(context_text)
        payload = {
            "entity_id": entity_id,
            "context_text": context_text,
            "mongo_collection": mongo_collection,
            "redis_key": redis_key,
            "neo4j_node_id": neo4j_node_id,
            **(metadata or {})
        }
        return self.connector.upsert_point(point_id=point_id, vector=vector, payload=payload)

    def search_entities(self, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Finds entities across all storage engines matching semantic intent."""
        query_vector = self.embedder.embed_text(query_text, prompt_name="query")
        return self.connector.search_similar(query_vector, limit=limit)

semantic_registry = UniversalSemanticRegistry()
