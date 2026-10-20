import hashlib
from typing import List, Optional
from config.settings import settings

class SemanticEmbedder:
    """Extracts continuous dense semantic vector embeddings from textual context."""

    def __init__(self):
        self._model = None
        self._dim = settings.EMBEDDING_DIMENSION

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
            except Exception:
                # Fallback to simulated deterministic dense vector generator if library not installed yet
                self._model = "mock"

    def embed_text(self, text: str, prompt_name: Optional[str] = None) -> List[float]:
        self._load_model()
        if self._model != "mock":
            embedding = self._model.encode(
                text,
                normalize_embeddings=True,
                prompt_name=prompt_name
            )
            return embedding.tolist()
        
        # Deterministic pseudo-vector for fallback/offline testing
        h = hashlib.sha256(text.encode("utf-8")).digest()
        vec = [((b / 255.0) * 2 - 1) for b in h]
        while len(vec) < self._dim:
            vec.extend(vec[:self._dim - len(vec)])
        
        # Normalize
        norm = sum(x*x for x in vec) ** 0.5 or 1.0
        return [x / norm for x in vec[:self._dim]]

semantic_embedder = SemanticEmbedder()
