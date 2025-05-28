# #src/routers/llm_chat.py

from fastapi import APIRouter, Request

from llm_core import call_gemini

from llm_core.vectordb import retrieve_similar_docs
# from gitingest.parse_query import retrun_uuid

router = APIRouter(prefix="/api/llm")  # Add prefix to avoid conflicts



def call_llm_model(text: str, question: str, model: str, api_key: str) -> str:
    if model.startswith("gemini"):
        return call_gemini(model, api_key, text, question)
    else:
        return f"Unknown model '{model}'"

@router.post("/v1/chat/completions")
async def run_local_llm_function(request: Request):
    data = await request.json()

    required_fields = [ "ingest_id", "question", "model", "api_key"]
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing field: {field}"}

    # Step 1: Retrieve similar documents using the question
    # similar_docs = retrieve_similar_docs(question=data["question"])
    collection_name= data.get('ingest_id') #"default"  # Assuming a default collection name, can be parameterized
    similar_docs = retrieve_similar_docs(collection_name, query=data["question"])
    # print(f"Retrieved {len(similar_docs)} similar documents for question: {data['question']}")

    # Step 2: Append retrieved context to input_text (optional strategy)
    context_text = "\n\n".join(similar_docs)
    combined_input = f"{context_text}"

    # Step 3: Call the LLM
    result = call_llm_model(
        text=combined_input,
        question=data["question"],
        model=data["model"],
        api_key=data["api_key"]
    )
    return {"response": result}
