# 📄 Document Intelligence Chatbot

> Upload documents. Ask questions. Get cited answers — powered by RAG + Groq LLaMA 3.

![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-orange)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F55036?logo=groq&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 🚀 Overview

A full-stack AI chatbot that allows users to upload documents (PDF, TXT, images) and ask natural-language questions about their contents.

It uses **Retrieval-Augmented Generation (RAG)** to return accurate, context-aware answers with source citations and key theme extraction.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 Multi-format Upload | PDF, TXT, PNG, JPG, BMP — drag & drop supported |
| 🔍 Semantic Search | Vector embeddings via SentenceTransformers + ChromaDB |
| 🤖 LLM Q&A | Context-aware answers from Groq LLaMA 3.1 |
| 📑 Citations | Every answer includes a page/paragraph source reference |
| 🎨 Theme Extraction | Key themes identified from each answer |
| 🌙 Dark Mode | Automatically respects OS dark mode preference |
| 📱 Responsive | Works on desktop, tablet, and mobile |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18 (Create React App), Vanilla CSS |
| **Backend** | FastAPI (Python 3.9+) |
| **Vector DB** | ChromaDB |
| **Embeddings** | SentenceTransformers `all-MiniLM-L6-v2` |
| **LLM** | Groq API — `llama-3.1-8b-instant` |
| **OCR** | Tesseract + pytesseract |
| **PDF Parsing** | PyMuPDF (fitz) |

---

## ⚙️ Local Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (for image uploads)
- A free [Groq API key](https://console.groq.com)

---

### 1. Clone the repo

```bash
git clone https://github.com/your-username/Document-Research-ChatBot.git
cd Document-Research-ChatBot/document-intelligence-chatbot
```

> ℹ️ The app lives inside the `document-intelligence-chatbot/` subfolder of the repo.

### 2. Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Activate — Windows (PowerShell):
venv\Scripts\activate
# Activate — macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Windows (PowerShell):
copy .env.example .env
# macOS / Linux:
cp .env.example .env

# Open .env in any text editor and set your Groq API key:
# GROQ_API_KEY=your_key_here

# Start the server
uvicorn app:app --reload --port 8000
```

✅ Backend running at `http://localhost:8000`  
📖 Interactive API docs at `http://localhost:8000/docs`

### 3. Frontend

Open a **second terminal**, then:

```bash
cd Document-Research-ChatBot/document-intelligence-chatbot/frontend
npm install
npm start
```

✅ App running at `http://localhost:3000`

> The frontend `package.json` sets `"proxy": "http://localhost:8000"`, so all `/upload/`, `/ask/`, and `/documents/` API calls are automatically forwarded to the backend in dev mode — no CORS issues.

---

## 📁 Project Structure

```
Document-Research-ChatBot/               ← GitHub repo root
├── README.md
|
└── document-intelligence-chatbot/       ← app source
    ├── .gitignore
    ├── backend/
    │   ├── .env.example                 # ← copy to .env, add GROQ_API_KEY
    │   ├── app.py                       # FastAPI entry point
    │   ├── requirements.txt
    │   ├── ingestion/
    │   │   └── document_ingestor.py     # PDF / image / text extraction
    │   ├── processing/
    │   │   ├── qa_engine.py             # RAG pipeline + Groq LLM
    │   │   └── summarizer.py            # AI document summarization
    │   └── utils/
    │       └── vector_store.py          # ChromaDB wrapper
    └── frontend/
        ├── package.json
        ├── public/
        │   ├── index.html
        │   ├── favicon.svg
        │   └── manifest.json
        └── src/
            ├── App.jsx
            ├── index.js
            ├── components/
            │   ├── ChatWindow.jsx
            │   ├── DocumentUploader.jsx
            │   └── ErrorBoundary.jsx
            └── styles/
                └── main.css
```

---

## 🔑 Environment Variables

Create `document-intelligence-chatbot/backend/.env` by copying the example template:

```bash
# Windows (PowerShell)
copy document-intelligence-chatbot\backend\.env.example document-intelligence-chatbot\backend\.env

# macOS / Linux
cp document-intelligence-chatbot/backend/.env.example document-intelligence-chatbot/backend/.env
```

Then open the file and set:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at 👉 https://console.groq.com

---

## 🔄 How It Works

```
User uploads document
       ↓
Text extracted (PDF → PyMuPDF, Image → Tesseract, TXT → UTF-8)
       ↓
Text split into overlapping chunks (300 words, 50-word overlap)
       ↓
Each chunk embedded with all-MiniLM-L6-v2 → stored in ChromaDB
       ↓
User asks a question
       ↓
Question embedded → top-5 similar chunks retrieved from ChromaDB
       ↓
Groq LLaMA 3.1 generates answer from retrieved context
       ↓
Answer + citation + themes returned to UI
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/upload/` | Upload documents (multipart/form-data) |
| `GET` | `/documents/` | List all uploaded documents |
| `POST` | `/ask/` | Ask a question (fields: `question`, `documentIds`) |
| `GET` | `/summarize/` | AI summary of all documents |

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m 'Add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---


