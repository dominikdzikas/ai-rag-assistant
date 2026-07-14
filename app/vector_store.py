from dataclasses import dataclass
import numpy as np
from sentence_transformers import SentenceTransformer


@dataclass
class SearchResult:
    text: str
    score: float


class InMemoryVectorStore:
    def __init__(self) -> None:
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.chunks: list[str] = []
        self.embaddings: np.array | None = None

    def add_documents(self, chunks: list[str]) -> None:
        self.chunks = chunks

        self.embeddings = self.model.encode(
            chunks,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        if self.embeddings is None or not self.chunks:
            return []
            
        query_embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores = self.embeddings @ query_embedding

        top_indices = np.argsort(scores)[::-1][:top_k]

        results: list[SearchResult] = []

        for idx in top_indices:
            results.append(
                SearchResult(
                    text=self.chunks[idx],
                    score=float(scores[idx])
                )
            )

        return results