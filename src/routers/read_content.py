# src/routers/read_content.py

import os
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from config import TMP_BASE_PATH  # Dynamically importing TMP path from config

router = APIRouter(prefix="/api/llm")


def read_content(ingest_id: str) -> str:
    """
    Function to read the content from a .txt file for a given 'ingest_id'.
    
    Parameters:
    - ingest_id (str): The unique ID to locate the corresponding text file.
    
    Returns:
    - str: The content of the .txt file.
    
    Raises:
    - HTTPException: If the directory or file is not found.
    """
    try:
        # Dynamically build the directory path from TMP_BASE_PATH and ingest_id
        directory = os.path.join(TMP_BASE_PATH, ingest_id)

        # Check if the directory exists
        if not os.path.isdir(directory):
            raise FileNotFoundError("Directory not found")

        # Find all .txt files in the directory
        txt_files = [f for f in os.listdir(directory) if f.endswith(".txt")]

        if not txt_files:
            raise FileNotFoundError("No .txt file found")

        # Read the content of the first .txt file found
        txt_file_path = os.path.join(directory, txt_files[0])
        with open(txt_file_path, "r") as file:
            content = file.read()

        return content

    except FileNotFoundError as e:
        # Raise HTTPException if file or directory is not found
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        # Catch any other errors (e.g., permission errors, unexpected errors)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/v1/retrieve/get_content")
async def retrieve_content(request: Request):
    data = await request.json()

    # Ensure 'ingest_id' is present in the request
    required_fields = ["ingest_id"]
    for field in required_fields:
        if field not in data:
            return JSONResponse(status_code=400, content={"error": f"Missing field: {field}"})

    # Retrieve content using the 'ingest_id'
    ingest_id = data["ingest_id"]
    try:
        result = read_content(ingest_id)
        return {"text": result}

    except HTTPException as e:
        # If there's an error reading the content, it will raise an HTTPException
        raise e

    except Exception as e:
        # Handle any other errors gracefully
        return JSONResponse(status_code=500, content={"error": f"An unexpected error occurred: {str(e)}"})
