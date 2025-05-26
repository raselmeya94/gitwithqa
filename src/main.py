

# main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.trustedhost import TrustedHostMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.routing import Route, Mount
from routers import download, dynamic, index, read_content, llm_chat_router

from server_utils import limiter

# Load environment variables
load_dotenv()

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
    for route in app.router.routes:
        if isinstance(route, Route):
            print(f"Route: {route.path} - Methods: {route.methods} - Name: {route.name}")
        elif isinstance(route, Mount):
            print(f"Mount: {route.path} - Mounted App: {route.app}")
            
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
    return {"status": "healthy"}

@app.head("/")
async def head_root() -> HTMLResponse:
    return HTMLResponse(content=None, headers={"content-type": "text/html; charset=utf-8"})

@app.get("/api/", response_class=HTMLResponse)
@app.get("/api", response_class=HTMLResponse)
async def api_docs(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("api.jinja", {"request": request})

@app.get("/robots.txt")
async def robots() -> FileResponse:
    return FileResponse("static/robots.txt")
