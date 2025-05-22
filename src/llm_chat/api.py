# # llm_chat/api.py
# import os
# from fastapi import APIRouter, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

# router = APIRouter()

# TMP_BASE_PATH = "../../tmp"  # Make sure this is aligned with llm_chat/api.py

# @router.get("/read_text/{digest_id}")
# async def read_text_file(digest_id: str):
#     directory = os.path.join(TMP_BASE_PATH, digest_id)
#     txt_files = [f for f in os.listdir(directory) if f.endswith(".txt")]
#     if not txt_files:
#         return {"error": "No text files found."}

#     with open(os.path.join(directory, txt_files[0]), "r", encoding="utf-8") as f:
#         return {"text": f.read()}
