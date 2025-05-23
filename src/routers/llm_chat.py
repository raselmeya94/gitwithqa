# #src/routers/llm_chat.py


from fastapi import APIRouter, Request
import google.generativeai as genai
# ----------------------------------------------------------------------
# AI API configuration
# ----------------------------------------------------------------------
# # Gemini
# GEMINI_API_KEY = "AIzaSyAcVe_hYiuloadI54nwIAaTUI86Cm25U1k"
# genai.configure(api_key=GEMINI_API_KEY)
# gemini_model = genai.GenerativeModel("gemini-2.0-flash")


# ----------------------------------------------------------------------
# Gemini backend
# ----------------------------------------------------------------------
def gemini_llm_api(api_key:str, text_data: str, input_prompt: str) -> str:
    """
    Generate answer using Gemini flash model.
    """
    # Set the API key
    genai.configure(api_key=api_key)
    # Initialize the model
    gemini_model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"{input_prompt}\n\n---\n\nContent:\n{text_data}"

    try:
        response = gemini_model.generate_content(prompt)
        return response.text

    except Exception:                                    
        return {
                "status": "error",
                "message": "Error while generating with Gemini.",
            }



router = APIRouter(prefix="/api/llm")  # Add prefix to avoid conflicts

def call_llm_model(text: str, question: str, model: str, api_key: str) -> str:
    if model == "gemini-2.0-flash":
        return gemini_llm_api(api_key, text, question)
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