from fastapi import APIRouter, HTTPException
from src.api.schemas import EntityIndexRequest, SemanticQueryRequest, DirectLookupRequest, HealthResponse
from src.storage_connectors.mongo_connector import mongo_connector
from src.storage_connectors.redis_connector import redis_connector
from src.storage_connectors.neo4j_connector import neo4j_connector
from src.storage_connectors.qdrant_connector import qdrant_connector
from src.semantic_indexing.vector_registry import semantic_registry
from src.mesh_core.planner import mesh_planner
from src.mesh_core.synthesizer import mesh_synthesizer
from src.adaptive_engine.telemetry import telemetry_tracker

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    """Checks connection health across all four non-relational database engines."""
    engines = {
        "mongodb": mongo_connector.ping(),
        "redis": redis_connector.ping(),
        "neo4j": neo4j_connector.ping(),
        "qdrant": qdrant_connector.ping()
    }
    overall_status = "healthy" if all(engines.values()) else "degraded"
    return HealthResponse(status=overall_status, engines=engines)

@router.post("/index/entity")
def index_entity(req: EntityIndexRequest):
    """Ingests and indexes an entity into MongoDB, Neo4j, and the Universal Semantic Vector Index."""
    # 1. Store Document in MongoDB
    doc_payload = req.document_data or {"id": req.entity_id, "description": req.context_text}
    doc_payload["id"] = req.entity_id
    mongo_connector.insert_document(req.mongo_collection, doc_payload)

    # 2. Synchronize Node in Neo4j Graph
    name = doc_payload.get("name", req.entity_id)
    category = doc_payload.get("category", "General")
    neo4j_synced = False
    try:
        # Create or update the entity node in Neo4j
        neo4j_connector.execute_cypher(
            """
            MERGE (e:Entity:Product {id: $id})
            SET e.name = $name, e.category = $category
            """,
            {"id": req.entity_id, "name": name, "category": category}
        )

        # If user passed explicit graph relationships, create them
        if req.graph_connections:
            for conn in req.graph_connections:
                target_id = conn.get("target_id")
                rel_type = conn.get("relation", "RELATED_TO").upper()
                if target_id:
                    cypher_rel = f"""
                    MATCH (e:Product {{id: $id}})
                    MERGE (t:Entity {{id: $target_id}})
                    MERGE (e)-[r:{rel_type}]->(t)
                    """
                    neo4j_connector.execute_cypher(cypher_rel, {"id": req.entity_id, "target_id": target_id})
        neo4j_synced = True
    except Exception as e:
        print(f"[Warning] Failed to sync entity to Neo4j: {e}")

    # 3. Index in Universal Vector Registry (Qdrant)
    success = semantic_registry.index_entity(
        point_id=req.point_id,
        context_text=req.context_text,
        entity_id=req.entity_id,
        mongo_collection=req.mongo_collection,
        redis_key=f"hot_cache:{req.entity_id}",
        neo4j_node_id=req.entity_id
    )

    return {
        "status": "indexed",
        "entity_id": req.entity_id,
        "mongodb_saved": True,
        "neo4j_synced": neo4j_synced,
        "semantic_vector_indexed": success
    }

@router.post("/query/semantic")
def semantic_query(req: SemanticQueryRequest):
    """Executes a semantic search and synthesizes hydrated entities from multiple stores."""
    results = mesh_synthesizer.semantic_query_and_hydrate(req.query, limit=req.limit)
    return {"query": req.query, "results_count": len(results), "data": results}

@router.post("/query/lookup")
def direct_lookup(req: DirectLookupRequest):
    """Performs an adaptive entity lookup, leveraging hot-cache routing when applicable."""
    result = mesh_planner.execute_entity_lookup(req.entity_id, collection=req.collection)
    return {"entity_id": req.entity_id, "result": result}

@router.get("/telemetry/stats")
def get_telemetry_stats():
    """Returns query latency distributions and hotspot stats used by the Adaptive Engine."""
    return telemetry_tracker.get_stats()
