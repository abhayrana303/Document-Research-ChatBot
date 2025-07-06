import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF
from vector_store import vector_store
import re

class DocumentIngestor:
    def __init__(self):
        self.documents = []

    def add_document(self, doc_id, filename, content):
        ext = filename.lower().split('.')[-1]
        if ext in ["jpg", "jpeg", "png", "bmp"]:
            text = self.extract_text_from_image(content)
        elif ext == "pdf":
            text = self.extract_text_from_pdf(content)
        else:
            try:
                text = content.decode("utf-8")
            except Exception:
                text = ""
        self.documents.append({
            "id": doc_id,
            "filename": filename,
            "text": text
        })
        # --- Vector DB integration ---
        chunks = self.split_into_chunks(text)
        vector_store.add_document_chunks(doc_id, chunks)

    def split_into_chunks(self, text, chunk_size=300, overlap=50):
        # Split text into chunks of chunk_size words with overlap
        words = re.split(r'(\s+)', text)
        chunks = []
        i = 0
        chunk_id = 0
        while i < len(words):
            chunk_words = words[i:i+chunk_size]
            chunk_text = ''.join(chunk_words).strip()
            if chunk_text:
                chunks.append({"text": chunk_text, "chunk_id": chunk_id})
                chunk_id += 1
            i += chunk_size - overlap
        return chunks

    def extract_text_from_image(self, content):
        image = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(image)

    def extract_text_from_pdf(self, content):
        text = ""
        with fitz.open(stream=content, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text

    def get_documents(self, ids=None):
        if ids:
            return [doc for doc in self.documents if doc["id"] in ids]
        return self.documents

    def summarize_documents(self):
        # Placeholder for summarization logic
        return "Summary of documents"