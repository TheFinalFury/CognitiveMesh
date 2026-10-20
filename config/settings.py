import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "CognitiveDataMesh"
    APP_ENV: str = "development"
    API_PORT: int = 8000
    DEBUG: bool = True

    # MongoDB
    MONGO_URI: str = "mongodb://localhost:27018/?replicaSet=rs0&directConnection=true"
    MONGO_DB_NAME: str = "cognitive_mesh"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password123"

    # Qdrant
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "universal_semantic_index_qwen3"

    # Semantic Embeddings
    EMBEDDING_MODEL_NAME: str = "Qwen/Qwen3-Embedding-0.6B"
    EMBEDDING_DIMENSION: int = 1024

    # Adaptive Engine
    CACHE_HOT_THRESHOLD: int = 5
    CACHE_TTL_SECONDS: int = 300

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
