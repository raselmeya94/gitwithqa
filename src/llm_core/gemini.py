# llm_core/gemini.py

import google.generativeai as genai

# System message to guide Gemini for context-aware, accurate responses
system_message = """
You are an AI model designed to answer questions about the codebase of a GitHub repository. Your responses should be:

- **Accurate and relevant**: Provide answers that are directly related to the repository's code, documentation, and comments. Always base your answers on the information available in the codebase.
- **Context-aware**: Make sure you understand the context of the question and refer to the relevant code, functions, files, and modules when answering.
- **No hallucination**: Avoid generating responses that are not backed by the code or repository content. If the question is unclear or cannot be answered based on the provided context, acknowledge the limitation rather than guessing or making assumptions.
- **Clear and concise**: Answer the question in a straightforward and clear manner. If needed, explain concepts, code, or logic in simple terms without unnecessary jargon.
- **Provide explanations**: Whenever possible, explain the code or logic behind the answer. For example, if you reference a function, describe what it does and how it works within the codebase.
- **Error handling**: If there is an error or unclear code, provide troubleshooting advice or point out the problem rather than suggesting a solution that doesn't fit.
"""

def call_gemini(model_name: str, api_key: str, context: str, question: str) -> str:
    """
    Function to call Google Gemini API with dynamic model selection.
    
    Parameters:
    - api_key (str): The API key for Google Gemini.
    - context (str): The context to be used for question answering.
    - question (str): The question to be answered.
    - model_name (str): The model name for Gemini (default is 'gemini-model-v1').
    
    Returns:
    - str: The model's response to the question.
    """
    # Initialize the Gemini client
    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel(model_name)

    # Construct the prompt with system message, context, and question
    prompt = f"""
    {system_message}

    Given the context: {context}, answer the following question: {question}
    """
    
    # Call the Gemini API (model name can be customized)
    response = gemini_model.generate_content(prompt)
    
    # Return the response text
    return response.text
