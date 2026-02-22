from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct,
    PayloadSchemaType, Filter, FieldCondition, MatchValue
)
import os
import time
import uuid


# ──────────────────────────────────────────────
#  Ayurvedic collection names
# ──────────────────────────────────────────────
AYURVEDIC_COLLECTIONS = [
    "conditions",
    "herbs",
    "diet_guidelines",
    "yoga_practices",
    "precautions",
    "lifestyle",
    "progress_logs",
]

EMBED_DIM = 1536  # text-embedding-3-small dimension


def _make_client() -> QdrantClient:
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY")
    if not url:
        raise ValueError("QDRANT_URL environment variable is not set")
    return QdrantClient(url=url, api_key=api_key, timeout=60, prefer_grpc=False)


# ──────────────────────────────────────────────
#  Ayurvedic multi-collection storage
# ──────────────────────────────────────────────
class AyurvedicStorage:
    """
    Manages multiple specialised Qdrant collections for the Ayurvedic RAG system.

    Collections:
        conditions, herbs, diet_guidelines, yoga_practices,
        precautions, lifestyle, progress_logs
    """

    def __init__(self, max_retries: int = 3):
        last_error = None
        for attempt in range(max_retries):
            try:
                self.client = _make_client()
                self._ensure_collections()
                print("✅ AyurvedicStorage ready")
                return
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"⚠️  Attempt {attempt + 1} failed. Retrying in {wait_time}s…")
                    time.sleep(wait_time)
                else:
                    raise ConnectionError(
                        f"Failed to connect to Qdrant after {max_retries} attempts. "
                        f"Last error: {last_error}"
                    ) from last_error

    # ── Internal helpers ──────────────────────
    def _ensure_collections(self):
        for name in AYURVEDIC_COLLECTIONS:
            if not self.client.collection_exists(name):
                self.client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
                )
                # Index common filter fields
                for field in ("condition", "dosha", "type", "herb"):
                    try:
                        self.client.create_payload_index(
                            collection_name=name,
                            field_name=field,
                            field_schema=PayloadSchemaType.KEYWORD,
                        )
                    except Exception:
                        pass

    # ── Upsert ───────────────────────────────
    def upsert_knowledge(self, collection: str, entries: list[dict], vectors: list[list[float]]):
        """
        Upsert a list of knowledge entries with their embeddings.

        Each entry must contain at least {"id": str, "text": str} plus metadata fields.
        """
        if collection not in AYURVEDIC_COLLECTIONS:
            raise ValueError(f"Unknown collection: {collection}")

        points = []
        for i, entry in enumerate(entries):
            entry_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{collection}_{entry['id']}"))
            payload = {k: v for k, v in entry.items() if k != "id"}
            points.append(PointStruct(id=entry_id, vector=vectors[i], payload=payload))

        self.client.upsert(collection_name=collection, points=points)

    # ── Condition-based retrieval ─────────────
    def search_by_condition(
        self,
        collection: str,
        query_vector: list[float],
        condition: str,
        top_k: int = 3,
    ) -> list[dict]:
        """
        Search a collection filtered by condition name.
        Returns a list of payloads with text and metadata.
        """
        filt = Filter(
            must=[FieldCondition(key="condition", match=MatchValue(value=condition))]
        )
        results = self.client.query_points(
            collection_name=collection,
            query=query_vector,
            query_filter=filt,
            with_payload=True,
            limit=top_k,
        ).points

        return [getattr(r, "payload", {}) for r in results]

    def search_semantic(
        self,
        collection: str,
        query_vector: list[float],
        top_k: int = 3,
    ) -> list[dict]:
        """Pure semantic search without condition filter."""
        results = self.client.query_points(
            collection_name=collection,
            query=query_vector,
            with_payload=True,
            limit=top_k,
        ).points
        return [getattr(r, "payload", {}) for r in results]

    # ── Progress logs ─────────────────────────
    def log_progress(
        self,
        user_id: str,
        condition: str,
        week: int,
        progress_data: dict,
        vector: list[float],
    ) -> str:
        """Store a weekly progress log for a user."""
        log_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{user_id}_{condition}_w{week}_{time.time()}"))
        payload = {
            "user_id": user_id,
            "condition": condition,
            "week": week,
            "timestamp": int(time.time()),
            **progress_data,
        }
        self.client.upsert(
            collection_name="progress_logs",
            points=[PointStruct(id=log_id, vector=vector, payload=payload)],
        )
        return log_id

    def get_user_progress(self, user_id: str, condition: str) -> list[dict]:
        """Retrieve all progress logs for a specific user and condition."""
        try:
            filt = Filter(
                must=[
                    FieldCondition(key="user_id", match=MatchValue(value=user_id)),
                    FieldCondition(key="condition", match=MatchValue(value=condition)),
                ]
            )
            points, _ = self.client.scroll(
                collection_name="progress_logs",
                scroll_filter=filt,
                limit=100,
                with_payload=True,
            )
            logs = [getattr(p, "payload", {}) for p in points]
            return sorted(logs, key=lambda x: x.get("week", 0))
        except Exception:
            return []

    # ── Seeding ───────────────────────────────
    def is_seeded(self, collection: str) -> bool:
        """Check if a collection already has data."""
        try:
            info = self.client.get_collection(collection)
            return (info.points_count or 0) > 0
        except Exception:
            return False
