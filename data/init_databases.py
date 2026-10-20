"""
Bootstrap and Seed Script for the Cognitive Data Mesh.
Populates sample products, graph relationships, and semantic embeddings across MongoDB, Neo4j, and Qdrant.
"""

import sys
import os

# Add root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.storage_connectors.mongo_connector import mongo_connector
from src.storage_connectors.redis_connector import redis_connector
from src.storage_connectors.neo4j_connector import neo4j_connector
from src.storage_connectors.qdrant_connector import qdrant_connector
from src.semantic_indexing.vector_registry import semantic_registry

SAMPLE_PRODUCTS = [
    {
        "point_id": 1,
        "id": "prod_101",
        "name": "Quantum Pro Noise-Cancelling Headphones",
        "category": "Electronics",
        "price": 299.99,
        "description": "High-fidelity wireless over-ear headphones with adaptive active noise cancellation and 40-hour battery life."
    },
    {
        "point_id": 2,
        "id": "prod_102",
        "name": "ErgoDrive Mechanical Ergonomic Keyboard",
        "category": "Accessories",
        "price": 149.50,
        "description": "Split wireless mechanical keyboard with hot-swappable tactile switches and cushioned wrist rest."
    },
    {
        "point_id": 3,
        "id": "prod_103",
        "name": "AeroGrip Ultra-Light Gaming Mouse",
        "category": "Gaming",
        "price": 79.99,
        "description": "Ultra-lightweight honeycomb optical gaming mouse with 26000 DPI optical sensor and RGB illumination."
    }
]

def seed():
    print("Connecting to databases...")
    mongo_connector.connect()
    redis_connector.connect()
    neo4j_connector.connect()
    qdrant_connector.connect()

    print("\n1. Seeding MongoDB Documents...")
    for prod in SAMPLE_PRODUCTS:
        doc = prod.copy()
        point_id = doc.pop("point_id")
        mongo_connector.insert_document("products", doc)
        print(f"   Indexed document in MongoDB: {doc['name']}")

    print("\n2. Seeding Neo4j Graph Relationships...")
    try:
        # Create Nodes
        neo4j_connector.execute_cypher("""
            MERGE (u:User {id: 'usr_alex', name: 'Alex Rivera'})
            MERGE (p1:Product {id: 'prod_101', name: 'Quantum Pro Headphones'})
            MERGE (p2:Product {id: 'prod_102', name: 'ErgoDrive Keyboard'})
            MERGE (u)-[:PURCHASED {rating: 5}]->(p1)
            MERGE (u)-[:WISHLISTED]->(p2)
        """)
        print("   Graph nodes and relationships created in Neo4j.")
    except Exception as e:
        print(f"   [Notice] Neo4j seeding skipped or error (ensure container running): {e}")

    print("\n3. Indexing Entities into Universal Semantic Vector Space (Qdrant)...")
    try:
        for prod in SAMPLE_PRODUCTS:
            context = f"{prod['name']} - {prod['category']} - {prod['description']}"
            semantic_registry.index_entity(
                point_id=prod["point_id"],
                context_text=context,
                entity_id=prod["id"],
                mongo_collection="products",
                metadata={"category": prod["category"], "price": prod["price"]}
            )
            print(f"   Indexed vector embedding for: {prod['name']}")
    except Exception as e:
        print(f"   [Notice] Qdrant seeding skipped or error (ensure container running): {e}")

    print("\nSeeding routine completed.")

if __name__ == "__main__":
    seed()
