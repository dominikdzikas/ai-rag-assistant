from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from app.llm import generate_llm
from app.document_loader import extract_text_from_pdf
from app.text_splitter import chunk_text
from app.vector_store import InMemoryVectorStore


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    top_k: int = Field(default=3, ge=1, le=10)


app = FastAPI()

vector_store = InMemoryVectorStore()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/ask")
async def ask(request: AskRequest):
    answer = await generate_llm(request.question)
    return {
        "answer": answer
    }

@app.post("/documents/extract")
async def extract_document(file: UploadFile = File(...)):
    content = await file.read()
    text, page_count = extract_text_from_pdf(content)
    chunks = chunk_text(text)

    return {
        "filename": file.filename,
        "pages": page_count,
        "characters": len(text),
        "chunk_count": len(chunks),
        "chunk_previews": [
            chunk[:200] for chunk in chunks[:3]
        ],
    }

@app.post("/documents/index")
async def index_document(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="Only PDF files are supported.",
            )
    
    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )
    try:
        text, page_count = extract_text_from_pdf(content)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="The PDF could not be read.",
        ) from exc

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No extractable text was found in the PDF.",
        )
    
    chunks = chunk_text(text)

    vector_store.add_documents(chunks)

    return {
        "filename": file.filename,
        "pages": page_count,
        "characters": len(text),
        "chunk_count": len(chunks),
        "message": "Document indexed successfully.",
    }

@app.post("/search")
async def search(request: SearchRequest):
    results = vector_store.search(
        query=request.query,
        top_k=request.top_k,
        )

    return {
        "query": request.query,
        "results": [
            {
                "score": result.score,
                "text": result.text[:500],
            }
            for result in results
        ],
    }