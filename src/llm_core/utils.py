import google.generativeai as genai
# ----------------------------------------------------------------------
# AI API configuration
# ----------------------------------------------------------------------


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


