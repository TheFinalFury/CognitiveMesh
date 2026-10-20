from typing import Any, Dict, List, Optional
from neo4j import GraphDatabase, Driver
from config.settings import settings
from src.storage_connectors.base import BaseStorageConnector

class Neo4jConnector(BaseStorageConnector):
    """Connector for Neo4j Graph Database."""

    def __init__(self):
        self.driver: Optional[Driver] = None

    def connect(self) -> None:
        if not self.driver:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )

    def ping(self) -> bool:
        try:
            if not self.driver:
                self.connect()
            self.driver.verify_connectivity()
            return True
        except Exception:
            return False

    def execute_cypher(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not self.driver:
            self.connect()
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def close(self) -> None:
        if self.driver:
            self.driver.close()
            self.driver = None

neo4j_connector = Neo4jConnector()
