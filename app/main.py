"""
BookBridge API — Main application entry point.

A platform for buying/selling academic books and sharing study resources.
Built with FastAPI, SQLAlchemy, and JWT authentication.
"""

import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .database import engine, Base
from .middleware import setup_middleware

# Import all models so SQLAlchemy can create tables
from .models import User, Book, Resource  # noqa: F401

from .routers import auth, users, books, resources

# ─── Logging Configuration ────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("bookbridge")

# ─── Application Factory ──────────────────────────────────────────────
settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "**BookBridge** is a platform where students can buy/sell academic books "
        "and share study resources (notes, PDFs, assignments) in one centralized system.\n\n"
        "### Features\n"
        "- 📚 **Book Marketplace** — List, browse, and buy books with category & condition filters\n"
        "- 📝 **StudyVault** — Upload and share notes, PDFs, assignments\n"
        "- 🔐 **JWT Authentication** — Secure user accounts\n"
        "- 👤 **User Profiles** — College, year, and contact info\n"
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── Setup ─────────────────────────────────────────────────────────────
# Create all database tables
Base.metadata.create_all(bind=engine)

# Configure middleware
setup_middleware(app)

# ─── Register Routers ─────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(resources.router)


# ─── Root & Health Endpoints ───────────────────────────────────────────
from fastapi.responses import RedirectResponse

@app.get("/", tags=["System"], include_in_schema=False)
def root():
    """Redirect root to frontend."""
    return RedirectResponse(url="/frontend/index.html")


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {"status": "healthy", "version": settings.APP_VERSION}


# ─── Serve Frontend Static Files ──────────────────────────────────────
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")