"""EduGenie - Production-Level AI Learning Assistant
Main FastAPI Application Entry Point.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from routes.explain import router as explain_router
from routes.history import router as history_router
from routes.learning import router as learning_router
from routes.progress import router as progress_router
from routes.qa import router as qa_router
from routes.quiz import router as quiz_router
from routes.settings import router as settings_router
from routes.summarize import router as summarize_router

# Setup Logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("edugenie")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode...")
    logger.info(f"Gemini API Configured: {settings.is_gemini_configured()}")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title="EduGenie — AI-Powered Personalized Learning Assistant",
    description="A modern, production-grade AI educational companion for concepts, Q&A, quizzes, summaries, and roadmaps.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files & Templates
STATIC_DIR.mkdir(parents=True, exist_ok=True)
(STATIC_DIR / "css").mkdir(parents=True, exist_ok=True)
(STATIC_DIR / "js").mkdir(parents=True, exist_ok=True)
(STATIC_DIR / "assets").mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# Validation Error Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for error in exc.errors():
        loc = " -> ".join(str(l) for l in error.get("loc", []))
        msg = error.get("msg", "Invalid value")
        error_messages.append(f"{loc}: {msg}")
    friendly_msg = "; ".join(error_messages) if error_messages else "Invalid input provided."
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "data": None,
            "message": friendly_msg,
            "error_code": "VALIDATION_ERROR",
        },
    )


# General Exception Handler
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "data": None,
            "message": "Something went wrong. Please try again.",
            "error_code": "INTERNAL_SERVER_ERROR",
        },
    )


# Register API Routers
app.include_router(qa_router)
app.include_router(explain_router)
app.include_router(quiz_router)
app.include_router(summarize_router)
app.include_router(learning_router)
app.include_router(history_router)
app.include_router(progress_router)
app.include_router(settings_router)


# Health Check
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "gemini_ready": settings.is_gemini_configured(),
        "model": settings.GEMINI_MODEL,
    }


# Frontend App Root
@app.get("/", response_class=HTMLResponse)
async def render_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.APP_NAME,
            "is_gemini_configured": settings.is_gemini_configured(),
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
