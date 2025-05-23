# #src/routers/llm_chat.py

from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/llm")  # Add prefix to avoid conflicts



from llm_core import call_gemini

def call_llm_model(text: str, question: str, model: str, api_key: str) -> str:
    if model.startswith("gemini"):
        return call_gemini(model, api_key, text, question)
    else:
        return f"Unknown model '{model}'"


@router.post("/v1/chat/completions") # Now the full path will be /api/llm/response_gen
async def run_local_llm_function(request: Request):
    data = await request.json()

    required_fields = ["input_text", "question", "model", "api_key"]
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing field: {field}"}

    result = call_llm_model(
        text=data["input_text"],
        question=data["question"],
        model=data["model"],
        api_key=data["api_key"]
    )
    return {"response": result}