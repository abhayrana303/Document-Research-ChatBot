import chromadb
#from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, persist_directory="chroma_db"):
        # self.client = chromadb.Client(Settings(
        #     persist_directory=persist_directory,
        #     chroma_db_impl="duckdb+parquet"
      #  ))
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection("documents")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def add_document_chunks(self, doc_id, chunks):
        # Each chunk is a dict: {"text": ..., "chunk_id": ...}
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [{"doc_id": doc_id, "chunk_id": chunk["chunk_id"]} for chunk in chunks]
        ids = [f"{doc_id}_{chunk['chunk_id']}" for chunk in chunks]
        embeddings = self.model.encode(texts).tolist()
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )

    def query_similar_chunks(self, query, top_k=5):
        query_embedding = self.model.encode([query])[0].tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        # Return list of dicts: {"text": ..., "doc_id": ..., "chunk_id": ...}
        return [
            {
                "text": doc,
                "doc_id": meta["doc_id"],
                "chunk_id": meta["chunk_id"]
            }
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]

vector_store = VectorStore()
