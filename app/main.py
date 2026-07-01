from fastapi import FastAPI
from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask(request: AskRequest):
    return {"answer": f"You're question was {request.question}"}