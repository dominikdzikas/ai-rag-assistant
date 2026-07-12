import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI()

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

async def generate_llm(question: str) -> str:
    response = await client.responses.create(
        model=MODEL_NAME,
        instructions=(
            "You are a concise and helpful AI assistant."
            "Answer in the same language as the user's question."
    ),
        input=question,
        
    )
    return response.output_text