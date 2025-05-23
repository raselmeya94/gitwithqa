# import os
# # main.py (top of the file)
# import logging

# from api_analytics.fastapi import Analytics
# from dotenv import load_dotenv
# from fastapi import FastAPI, Request
# from fastapi.responses import FileResponse, HTMLResponse, Response
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from slowapi import _rate_limit_exceeded_handler
# from slowapi.errors import RateLimitExceeded
# from starlette.middleware.trustedhost import TrustedHostMiddleware

# from routers import download, dynamic, index , read_text
# from llm_chat import api as llm_chat_router  # NEW
# from server_utils import limiter

# load_dotenv()

# app = FastAPI()
# app.state.limiter = limiter

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("app.log", mode='a', encoding='utf-8'),
#         logging.StreamHandler()
#     ],
#     force=True  # This is key! It resets any previous configs
# )

# # Define a wrapper handler with the correct signature
# async def rate_limit_exception_handler(request: Request, exc: Exception) -> Response:
#     if isinstance(exc, RateLimitExceeded):
#         # Delegate to the actual handler
#         return _rate_limit_exceeded_handler(request, exc)
#     # Optionally, handle other exceptions or re-raise
#     raise exc


# # Register the wrapper handler
# app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# app_analytics_key = os.getenv("API_ANALYTICS_KEY")
# if app_analytics_key:
#     app.add_middleware(Analytics, api_key=app_analytics_key)

# # Define the default allowed hosts
# default_allowed_hosts = [ "*"]

# # Fetch allowed hosts from the environment variable or use the default
# allowed_hosts = os.getenv("ALLOWED_HOSTS")
# if allowed_hosts:
#     allowed_hosts = allowed_hosts.split(",")
# else:
#     allowed_hosts = default_allowed_hosts

# app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
# templates = Jinja2Templates(directory="templates")


# @app.get("/health")
# async def health_check() -> dict[str, str]:
#     return {"status": "healthy"}


# @app.head("/")
# async def head_root() -> HTMLResponse:
#     """Mirror the headers and status code of the index page"""
#     return HTMLResponse(content=None, headers={"content-type": "text/html; charset=utf-8"})


# @app.get("/api/", response_class=HTMLResponse)
# @app.get("/api", response_class=HTMLResponse)
# async def api_docs(request: Request) -> HTMLResponse:
#     return templates.TemplateResponse("api.jinja", {"request": request})


# @app.get("/robots.txt")
# async def robots() -> FileResponse:
#     return FileResponse("static/robots.txt")


# app.include_router(index)
# app.include_router(download)
# app.include_router(dynamic)

# app.include_router(read_text)


# # # ✅ Include the new LLM Chat API
# # app.include_router(llm_chat_router.router)

# # from llm_chat.api import router as llm_chat_router  # or correct path to where you placed the function

# # app.include_router(llm_chat_router)



# main.py
import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.trustedhost import TrustedHostMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from routers import download, dynamic, index, read_content, llm_chat_router

from server_utils import limiter

# Load environment variables
load_dotenv()

# ✅ Logging setup (global)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ],
    force=True  # reset previous logging setup
)
logger = logging.getLogger()  # root logger
logger.info("🚀 Starting FastAPI application...")

# ✅ Initialize FastAPI app
app = FastAPI()
app.state.limiter = limiter

# ✅ Rate limit exception handler
async def rate_limit_exception_handler(request: Request, exc: Exception) -> Response:
    if isinstance(exc, RateLimitExceeded):
        return _rate_limit_exceeded_handler(request, exc)
    raise exc

app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

# ✅ Setup static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ✅ Setup Trusted Host Middleware

# ✅ Setup Trusted Host Middleware
default_allowed_hosts = ["*"]
allowed_hosts = os.getenv("ALLOWED_HOSTS", "*").split(",")
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# Improved route debugging
@app.on_event("startup")
async def debug_routes():
    logger.info("🛣️ Registered routes:")
    for route in app.routes:
        if hasattr(route, "path"):
            # Handle both regular routes and Mount objects
            if hasattr(route, "methods"):
                logger.info(f"Route: {route.path} - Methods: {route.methods}")
            elif hasattr(route, "name"):
                logger.info(f"Mount: {route.path} -> {route.name}")
            else:
                logger.info(f"Path: {route.path}")

# Include routers in the correct order
app.include_router(index)
app.include_router(download)
app.include_router(read_content)  # Read content routes first
app.include_router(llm_chat_router)  # LLM routes first
app.include_router(dynamic)
# ✅ Include routers
# logger.info("🔌 Including routers...")
# app.include_router(index)
# app.include_router(download)
# app.include_router(dynamic)
# app.include_router(llm_chat_router)
# logger.info("✅ Routers included successfully.")

# ✅ Health check and other endpoints
@app.get("/health")
async def health_check() -> dict[str, str]:
    logger.info("📍 Health check endpoint hit")
    return {"status": "healthy"}

@app.head("/")
async def head_root() -> HTMLResponse:
    return HTMLResponse(content=None, headers={"content-type": "text/html; charset=utf-8"})

@app.get("/api/", response_class=HTMLResponse)
@app.get("/api", response_class=HTMLResponse)
async def api_docs(request: Request) -> HTMLResponse:
    logger.info("📍 API docs requested")
    return templates.TemplateResponse("api.jinja", {"request": request})

@app.get("/robots.txt")
async def robots() -> FileResponse:
    return FileResponse("static/robots.txt")
