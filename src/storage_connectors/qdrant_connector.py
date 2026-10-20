from typing import Any, Dict, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from config.settings import settings
from src.storage_connectors.base import BaseStorageConnector

class QdrantConnector(BaseStorageConnector):
    """Connector for Qdrant Vector Database (Semantic Indexing Fabric)."""

    def __init__(self):
        self.client: Optional[QdrantClient] = None

    def connect(self) -> None:
        if not self.client:
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
                timeout=2.0,
                check_compatibility=False
            )

    def ping(self) -> bool:
        try:
            if not self.client:
                self.connect()
            self.client.get_collections()
            return True
        except Exception:
            return False

    def ensure_collection(self, collection_name: Optional[str] = None) -> None:
        if not self.client:
            self.connect()
        col = collection_name or settings.QDRANT_COLLECTION
        collections = [c.name for c in self.client.get_collections().collections]
        if col not in collections:
            self.client.create_collection(
                collection_name=col,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE
                )
            )

    def upsert_point(self, point_id: int, vector: List[float], payload: Dict[str, Any], collection_name: Optional[str] = None) -> bool:
        if not self.client:
            self.connect()
        col = collection_name or settings.QDRANT_COLLECTION
        self.ensure_collection(col)
        self.client.upsert(
            collection_name=col,
            points=[PointStruct(id=point_id, vector=vector, payload=payload)]
        )
        return True

    def search_similar(self, query_vector: List[float], limit: int = 5, collection_name: Optional[str] = None) -> List[Dict[str, Any]]:
        if not self.client:
            self.connect()
        col = collection_name or settings.QDRANT_COLLECTION
        self.ensure_collection(col)
        
        # Support both new query_points and legacy search APIs
        if hasattr(self.client, "query_points"):
            response = self.client.query_points(
                collection_name=col,
                query=query_vector,
                limit=limit
            )
            hits = response.points
        else:
            hits = self.client.search(
                collection_name=col,
                query_vector=query_vector,
                limit=limit
            )
        return [{"id": h.id, "score": getattr(h, "score", 0.0), "payload": h.payload} for h in hits]

    def close(self) -> None:
        self.client = None

qdrant_connector = QdrantConnector()
