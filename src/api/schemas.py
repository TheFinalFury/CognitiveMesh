from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class EntityIndexRequest(BaseModel):
    point_id: int
    entity_id: str
    context_text: str
    mongo_collection: str = "products"
    document_data: Optional[Dict[str, Any]] = None
    graph_connections: Optional[List[Dict[str, Any]]] = None

class SemanticQueryRequest(BaseModel):
    query: str = Field(..., description="Natural language or conceptual search prompt")
    limit: int = Field(default=5, ge=1, le=50)

class DirectLookupRequest(BaseModel):
    entity_id: str
    collection: str = "products"

class HealthResponse(BaseModel):
    status: str
    engines: Dict[str, bool]
