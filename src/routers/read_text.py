# # routers/read_text.py
# import logging
# import os
# from fastapi import APIRouter, HTTPException
# from fastapi.responses import PlainTextResponse

# from config import TMP_BASE_PATH

# router = APIRouter()

# @router.get("/read_text/{digest_id}", response_class=PlainTextResponse)
# async def read_text_file(digest_id: str):
#     try:
#         directory = os.path.join(TMP_BASE_PATH, digest_id)
#         print(f"Directory: {directory}", flush=True)
#         txt_files = [f for f in os.listdir(directory) if f.endswith(".txt")]
#         print(f"Directory: {directory}", flush=True)
#         print(f"Files: {txt_files}", flush=True)

#         if not txt_files:
#             raise FileNotFoundError("No .txt file found")

#         file_path = os.path.join(directory, txt_files[0])

#         with open(file_path, "r", encoding="utf-8") as f:
#             content = f.read()

#         return content

#     except Exception as e:
#         raise HTTPException(status_code=404, detail=f"Error: {str(e)}")

# routers/read_text.py
import os
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
# from config import TMP_BASE_PATH
TMP_BASE_PATH = "../../tmp"  # Adjust this path as needed
logger = logging.getLogger()

router = APIRouter()

@router.get("/read_text/{digest_id}", response_class=PlainTextResponse)
async def read_text_file(digest_id: str):
    logger.info(f"📥 Requested to read text for ID: {digest_id}")
    file_path = os.path.join(TMP_BASE_PATH, digest_id, "raselmeya94-RAGpedia.txt")
    logger.info(f"📄 File path resolved: {file_path}")

    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError("File not found")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        logger.info("✅ File read successfully")
        return content

    except Exception as e:
        logger.error(f"❌ Error reading file: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error: {str(e)}")


# {% block extra_scripts %}

#     <script>
#     function handleLLMSubmit(ingestId) {
#         const question = document.getElementById('chat-input').value.trim();
#         const responseBox = document.getElementById('chat-response');
#         responseBox.innerText = 'Thinking...';

#         console.log(responseBox.innerText)

#         if (!question) {
#             responseBox.innerText = 'Please enter a question.';
#             return;
#         }

#         sendToLLM(ingest_id, question, (err, answer) => {
#             if (err) {
#                 responseBox.innerText = `Error somethings: ${err}`;
#             } else {
#                 responseBox.innerText = answer;
#             }
#         });
#     }

# async function retrieve_context(ingest_id) {
#     try {
#         const digestId = ingest_id;  // replace with dynamic value if needed
#         const response = await fetch(`/read_text/${digestId}`);
        
#         if (!response.ok) {
#             throw new Error("Failed to fetch context");
#         }

#         const text = await response.text();
#         console.log("Context text:", text);
#         return text;
#     } catch (err) {
#         console.error("Error retrieving context:", err);
#         return '';
#     }
# }
#     async function sendToLLM( ingest_id, question, callback) {
#     const text = await retrieve_context(ingest_id);  
#     console.log(text);
#     console.log(question);

#     try {
#         const response = await fetch('http://192.168.10.137:9000/api/btr_qa_follow_up', {
#             method: 'POST',
#             headers: {
#                 'Content-Type': 'application/json',
#             },
#             body: JSON.stringify({
#                 text: text,
#                 query: question
#             }),
#         });

#         const data = await response.json();

#         // Updated to match your API response structure
#         if (data && data.status === "success" && data.data && data.data.response) {
#             callback(null, data.data.response);
#         } else {
#             callback('No valid response from LLM');
#         }
#     } catch (error) {
#         console.error('LLM error:', error);
#         callback('LLM error occurred');
#     }
# }

# </script>

# {% endblock extra_scripts %}