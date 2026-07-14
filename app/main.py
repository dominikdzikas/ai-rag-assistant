from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, Field
from app.llm import generate_llm
from app.document_loader import extract_text_from_pdf
from app.text_splitter import chunk_text


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


app = FastAPI()


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