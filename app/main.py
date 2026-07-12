from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.llm import generate_llm


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
