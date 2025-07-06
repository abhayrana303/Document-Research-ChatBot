import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import uuid
import requests
from ingestion.document_ingestor import DocumentIngestor
from processing.qa_engine import QAEngine
from processing.summarizer import Summarizer

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_DOCUMENTS = 75
document_ingestor = DocumentIngestor()
qa_engine = QAEngine()

@app.post("/upload/")
async def upload_documents(files: List[UploadFile] = File(...)):
    try:
        current_docs = len(document_ingestor.get_documents())
        if current_docs + len(files) > MAX_DOCUMENTS:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum document limit ({MAX_DOCUMENTS}) would be exceeded. Current: {current_docs}"
            )

        file_ids = []
        for file in files:
            content = await file.read()
            doc_id = f"DOC{(len(document_ingestor.get_documents()) + 1):03d}"
            document_ingestor.add_document(doc_id, file.filename, content)
            file_ids.append(doc_id)
        return JSONResponse(content={"message": "Documents uploaded successfully.", "ids": file_ids}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.get("/documents/")
def list_documents():
    docs = document_ingestor.get_documents()
    return JSONResponse(content=docs, status_code=200)

@app.post("/ask/")
async def ask_question(question: str = Form(...), documentIds: List[str] = Form(None)):
    try:
        docs = document_ingestor.get_documents(documentIds)
        if not docs:
            return JSONResponse(content={"error": "No documents found"}, status_code=400)
        answers, themes = qa_engine.process_question(question, docs)
        return JSONResponse(content={"answers": answers, "themes": themes}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.get("/summarize/")
def summarize_documents():
    try:
        docs = document_ingestor.get_documents()
        summary = "\n".join([doc["filename"] for doc in docs])
        return JSONResponse(content={"summary": summary}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)