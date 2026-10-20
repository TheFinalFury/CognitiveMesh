from typing import Any, Dict, List
from src.mesh_core.planner import mesh_planner
from src.semantic_indexing.vector_registry import semantic_registry

class MeshResponseSynthesizer:
    """Synthesizes cross-model vector matches into fully populated entities."""

    def __init__(self):
        self.registry = semantic_registry
        self.planner = mesh_planner

    def semantic_query_and_hydrate(self, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Finds semantic matches and hydrates them with document details and graph edges."""
        matches = self.registry.search_entities(query_text, limit=limit)
        results = []

        for match in matches:
            payload = match.get("payload", {})
            entity_id = payload.get("entity_id")
            collection = payload.get("mongo_collection") or "products"

            if entity_id:
                hydrated = self.planner.execute_entity_lookup(entity_id, collection=collection)
                hydrated["_similarity_score"] = round(match.get("score", 0.0), 4)
                results.append(hydrated)

        return results

mesh_synthesizer = MeshResponseSynthesizer()
