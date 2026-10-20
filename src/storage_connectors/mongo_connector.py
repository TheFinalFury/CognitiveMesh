from typing import Any, Dict, List, Optional
from pymongo import MongoClient
from config.settings import settings
from src.storage_connectors.base import BaseStorageConnector

class MongoConnector(BaseStorageConnector):
    """Connector for MongoDB Document Store."""

    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db = None

    def connect(self) -> None:
        if not self.client:
            self.client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=2000)
            self.db = self.client[settings.MONGO_DB_NAME]

    def ping(self) -> bool:
        try:
            if not self.client:
                self.connect()
            self.client.admin.command("ping")
            return True
        except Exception:
            return False

    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> str:
        if not self.client:
            self.connect()
        result = self.db[collection_name].insert_one(document)
        return str(result.inserted_id)

    def find_by_id(self, collection_name: str, entity_id: str) -> Optional[Dict[str, Any]]:
        if not self.client:
            self.connect()
        doc = self.db[collection_name].find_one({"id": entity_id})
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def query(self, collection_name: str, filter_query: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        if not self.client:
            self.connect()
        cursor = self.db[collection_name].find(filter_query).limit(limit)
        results = []
        for doc in cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    def close(self) -> None:
        if self.client:
            self.client.close()
            self.client = None

mongo_connector = MongoConnector()
