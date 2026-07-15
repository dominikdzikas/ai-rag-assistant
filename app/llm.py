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

async def generate_answer_with_context(
        question: str,
        context: list[str],
) -> str:
    context_text = "\n\n---\n\n".join(
        f"Context {index + 1}:\n{context}"
        for index, context in enumerate(context)
    )

    prompt = f"""
Use the context below to answer the user's question.

Rules:
- Answer only based on the provided context.
- If the answer is not in the context, say that the document does not contain enough information.
- Answer in the same language as the user's question.
- Be concise and clear.

Context:
{context_text}

Question:
{question}
"""
    
    response = await client.responses.create(
        model=MODEL_NAME,
        instructions=(
            "You are a document-based AI assistant. "
            "You answer questions using only the provided context."
        ),
        input=prompt,
    )
    return response.output_text