from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from src.api.routes import router
from src.storage_connectors.mongo_connector import mongo_connector
from src.storage_connectors.redis_connector import redis_connector
from src.storage_connectors.neo4j_connector import neo4j_connector
from src.storage_connectors.qdrant_connector import qdrant_connector

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize connector pools
    print(f"[{settings.APP_NAME}] Initializing polyglot storage connectors...")
    mongo_connector.connect()
    redis_connector.connect()
    neo4j_connector.connect()
    qdrant_connector.connect()
    print(f"[{settings.APP_NAME}] Storage connectors ready.")
    yield
    # Shutdown: Close connector pools
    print(f"[{settings.APP_NAME}] Shutting down connectors...")
    mongo_connector.close()
    redis_connector.close()
    neo4j_connector.close()
    qdrant_connector.close()

app = FastAPI(
    title=settings.APP_NAME,
    description="Cognitive Data Mesh: Universal Semantic Indexing & Adaptive Polyglot Query Engine",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "framework": "Cognitive Data Mesh",
        "status": "online",
        "docs_url": "/docs",
        "health_check": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main.py:app", host="0.0.0.0", port=settings.API_PORT, reload=settings.DEBUG)
