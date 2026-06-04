import chromadb
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self, persist_directory="chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection("documents")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def add_document_chunks(self, doc_id, chunks):
        """Add document text chunks with their embeddings to ChromaDB."""
        if not chunks:
            return
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [{"doc_id": doc_id, "chunk_id": chunk["chunk_id"]} for chunk in chunks]
        ids = [f"{doc_id}_{chunk['chunk_id']}" for chunk in chunks]
        embeddings = self.model.encode(texts).tolist()
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings,
        )

    def query_similar_chunks(self, query: str, top_k: int = 5) -> list:
        """Query ChromaDB for the most semantically similar chunks to the query."""
        # Guard: if the collection is empty, return early to avoid IndexError
        count = self.collection.count()
        if count == 0:
            return []

        # Don't ask for more results than exist
        n_results = min(top_k, count)
        query_embedding = self.model.encode([query])[0].tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )

        if not results["documents"] or not results["documents"][0]:
            return []

        return [
            {
                "text": doc,
                "doc_id": meta["doc_id"],
                "chunk_id": meta["chunk_id"],
            }
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]


vector_store = VectorStore()
