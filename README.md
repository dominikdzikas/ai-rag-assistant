# AI RAG Assistant

A small FastAPI-based document question answering backend built to learn and demonstrate the core concepts of modern LLM applications, including PDF processing, text chunking, embeddings, vector search and Retrieval-Augmented Generation (RAG).

The application allows users to upload a PDF document, index its content, search for relevant document chunks and ask questions that are answered using an LLM based on the retrieved context.

## Features

* FastAPI backend with interactive Swagger documentation
* Basic health check endpoint
* LLM API integration
* PDF text extraction
* Text chunking with overlap
* Text normalization for noisy PDF extraction
* Local embedding generation using `sentence-transformers`
* In-memory vector search
* Retrieval-Augmented Generation endpoint
* Source snippets included in RAG responses
* Environment variable based configuration

## Tech Stack

* Python
* FastAPI
* Pydantic
* OpenAI API
* python-dotenv
* pypdf
* sentence-transformers
* NumPy
* Git

## Project Structure

```text
ai-rag-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── llm.py
│   ├── document_loader.py
│   ├── text_splitter.py
│   └── vector_store.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

The system follows a simple RAG pipeline:

```text
PDF document
    ↓
text extraction
    ↓
text normalization
    ↓
chunking
    ↓
embedding generation
    ↓
vector search
    ↓
retrieved context
    ↓
LLM answer
```

First, the user uploads a PDF document. The backend extracts its text, normalizes it and splits it into smaller overlapping chunks. Each chunk is converted into an embedding vector and stored in memory.

When the user asks a question, the question is also embedded and compared to the stored document chunks. The most relevant chunks are retrieved and passed to the LLM as context. The LLM then generates an answer based only on the retrieved document content.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/dominikdzikas/ai-rag-assistant.git
cd ai-rag-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create the environment file

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Add your API key:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

## Running the Application

Start the FastAPI development server:

```bash
fastapi dev app/main.py
```

Then open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

### Basic LLM Question Answering

```http
POST /ask
```

Example request:

```json
{
  "question": "Explain Retrieval-Augmented Generation in simple terms."
}
```

Example response:

```json
{
  "answer": "Retrieval-Augmented Generation is a method where an AI system first retrieves relevant information from external documents and then uses that information to generate a more grounded answer."
}
```

### Extract Text from PDF

```http
POST /documents/extract
```

Uploads a PDF and returns basic information about the extracted text, including the number of pages, character count and chunk previews.

Example response:

```json
{
  "filename": "cv.pdf",
  "pages": 1,
  "characters": 2200,
  "chunk_count": 3,
  "chunk_previews": [
    "Contact Information...",
    "Work Experience...",
    "Projects..."
  ]
}
```

### Index a PDF Document

```http
POST /documents/index
```

Uploads a PDF, extracts its text, splits it into chunks, generates embeddings and stores them in memory for later search.

Example response:

```json
{
  "filename": "cv.pdf",
  "pages": 1,
  "characters": 2200,
  "chunk_count": 3,
  "message": "Document indexed successfully."
}
```

### Search Indexed Document Chunks

```http
POST /search
```

Example request:

```json
{
  "query": "What machine learning experience is mentioned?",
  "top_k": 3
}
```

Example response:

```json
{
  "query": "What machine learning experience is mentioned?",
  "results": [
    {
      "score": 0.42,
      "text": "Implemented U-Net model in PyTorch for binary segmentation..."
    }
  ]
}
```

### RAG Question Answering

```http
POST /rag/ask
```

Example request:

```json
{
  "question": "What machine learning experience is mentioned?",
  "top_k": 3
}
```

Example response:

```json
{
  "question": "What machine learning experience is mentioned?",
  "answer": "The document mentions experience with PyTorch, U-Net, computer vision, road segmentation, OpenCV, IoU-based evaluation and data processing pipelines.",
  "sources": [
    {
      "score": 0.42,
      "text": "CNN-based Drivable Road Detection..."
    }
  ]
}
```

## Example Workflow

1. Start the application.
2. Open the Swagger documentation at `http://127.0.0.1:8000/docs`.
3. Upload a PDF using `POST /documents/index`.
4. Search the indexed document using `POST /search`.
5. Ask a document-based question using `POST /rag/ask`.

The document must be indexed before using the search or RAG endpoints.

## What I Learned

This project helped me understand the main building blocks of LLM-based applications:

* how to build a Python backend with FastAPI
* how request and response validation works with Pydantic
* how to call an LLM API from a backend service
* how to extract text from PDF files
* why document preprocessing and text normalization matter
* how chunking and overlap affect retrieval quality
* how embeddings represent semantic meaning
* how vector similarity search works
* how Retrieval-Augmented Generation combines search and generation
* how to return source snippets for more transparent AI answers

## Limitations

This is a learning-focused mini project, not a production-ready system.

Current limitations:

* the vector store is in-memory, so indexed documents are lost after server restart
* only PDF documents are supported
* scanned image-based PDFs are not handled because no OCR is implemented
* there is no authentication or user management
* only one active indexed document collection is handled at a time
* no persistent database is used

## Future Improvements

Possible next steps:

* add persistent vector storage using ChromaDB or FAISS
* support multiple uploaded documents
* add document metadata and source page numbers
* improve chunking using sentence-based or token-based splitting
* add Docker support
* deploy the application to Google Cloud Run
* add automated tests
* add a simple frontend
* experiment with MCP-based tool integration

## Status

This project was created as a short learning project to prepare for AI/ML internship roles focused on LLM applications, RAG systems, Python backend development and modern AI tooling.
