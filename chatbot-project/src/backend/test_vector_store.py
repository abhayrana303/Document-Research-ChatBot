from vector_store import vector_store

def test_vector_store():
    # Add some dummy chunks
    doc_id = "TESTDOC"
    chunks = [
        {"text": "This is a test chunk about AI and machine learning.", "chunk_id": 0},
        {"text": "Another chunk about FastAPI and Python backend development.", "chunk_id": 1},
        {"text": "ChromaDB is a vector database for semantic search.", "chunk_id": 2}
    ]
    vector_store.add_document_chunks(doc_id, chunks)
    # Query for a relevant chunk
    results = vector_store.query_similar_chunks("What is ChromaDB?", top_k=2)
    print("Query Results:")
    for res in results:
        print(res)

if __name__ == "__main__":
    test_vector_store()
