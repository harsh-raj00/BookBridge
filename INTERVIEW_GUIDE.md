# 📚 BookBridge — Complete Interview Preparation Guide

> **This document covers everything you need to explain BookBridge in a technical interview** — from high-level architecture to line-by-line code explanations, with 30+ interview Q&A.

---

## 📌 Table of Contents

1. [Project Overview](#-1-project-overview)
2. [Problem Statement & Motivation](#-2-problem-statement--motivation)
3. [Architecture Deep-Dive](#-3-architecture-deep-dive)
4. [Technology Choices — "Why X, Not Y?"](#-4-technology-choices--why-x-not-y)
5. [Library-by-Library Explanation](#-5-library-by-library-explanation)
6. [File-by-File & Function-by-Function Walkthrough](#-6-file-by-file--function-by-function-walkthrough)
7. [Database Design & ORM Concepts](#-7-database-design--orm-concepts)
8. [Authentication & Security Deep-Dive](#-8-authentication--security-deep-dive)
9. [API Design & RESTful Principles](#-9-api-design--restful-principles)
10. [Frontend Architecture](#-10-frontend-architecture)
11. [Testing Strategy](#-11-testing-strategy)
12. [DevOps & Deployment](#-12-devops--deployment)
13. [Interview Q&A (30+ Questions)](#-13-interview-qa-30-questions)

---

## 🎯 1. Project Overview

**BookBridge** is a **full-stack web application** that solves two problems for college students:

1. **Book Marketplace** — Buy and sell second-hand academic books (Engineering, Medical, Law, etc.)
2. **StudyVault** — Share and download study resources (notes, PDFs, assignments, question papers)

### Key Features:
| Feature | Description |
|---------|-------------|
| **User Auth** | JWT-based registration & login with bcrypt password hashing |
| **Book CRUD** | Create, Read, Update, Delete book listings with filters |
| **Resource Sharing** | Upload/download files with metadata tagging |
| **Search & Filter** | Full-text search, category/condition/price filters, pagination |
| **Owner Authorization** | Users can only edit/delete their own listings |
| **Auto Swagger Docs** | Interactive API documentation at `/docs` |

### Tech Stack Summary:
```
Backend:  Python 3.12 + FastAPI + SQLAlchemy + SQLite
Auth:     JWT (python-jose) + bcrypt (passlib)
Frontend: Vanilla HTML + CSS + JavaScript
Testing:  pytest + httpx + TestClient
DevOps:   Docker + docker-compose
```

---

## 💡 2. Problem Statement & Motivation

### The Problem:
> College students waste money buying expensive new textbooks and have no centralized place to share study materials.

### How BookBridge Solves It:
- **Peer-to-peer marketplace** — Students sell books they no longer need at lower prices
- **Resource hub** — Students upload and share notes, question papers, assignments
- **Category-based organization** — Filter by Engineering, Medical, Law, etc.
- **Semester/Subject tagging** — Find exact resources for specific courses

### Why This Project Stands Out in Interviews:
- Demonstrates **full-stack development** (backend API + frontend UI)
- Shows **authentication & authorization** (JWT, bcrypt, protected routes)
- Uses **industry-standard patterns** (MVC, service layer, dependency injection)
- Has **automated tests** (pytest, isolated test database)
- Includes **Docker containerization** (production-ready deployment)

---

## 🏗️ 3. Architecture Deep-Dive

### System Architecture Diagram:
```
┌──────────────────┐        HTTP/REST         ┌──────────────────────────┐
│                  │  ◄──────────────────────► │                          │
│    Frontend      │    JSON + JWT Bearer      │    FastAPI Backend        │
│  (HTML/CSS/JS)   │                           │                          │
│                  │                           │  ┌─────────────────────┐  │
│  - Login/Register│                           │  │     Routers         │  │
│  - Browse Books  │                           │  │  (auth, books,      │  │
│  - Sell Books    │                           │  │   resources, users) │  │
│  - StudyVault    │                           │  └─────────┬───────────┘  │
│                  │                           │            │              │
└──────────────────┘                           │  ┌─────────▼───────────┐  │
                                               │  │   Schemas (Pydantic)│  │
                                               │  │   - Validation      │  │
                                               │  │   - Serialization   │  │
                                               │  └─────────┬───────────┘  │
                                               │            │              │
                                               │  ┌─────────▼───────────┐  │
                                               │  │  Services           │  │
                                               │  │  - auth_service     │  │
                                               │  │  - file_service     │  │
                                               │  └─────────┬───────────┘  │
                                               │            │              │
                                               │  ┌─────────▼───────────┐  │
                                               │  │  Models (SQLAlchemy)│  │
                                               │  │  - User, Book,      │  │
                                               │  │    Resource          │  │
                                               │  └─────────┬───────────┘  │
                                               │            │              │
                                               │  ┌─────────▼───────────┐  │
                                               │  │  SQLite Database    │  │
                                               │  │  (bookbridge.db)    │  │
                                               │  └─────────────────────┘  │
                                               └──────────────────────────┘
```

### Folder Structure Explained:
```
BookBridge/
├── app/                     # ← Backend application package
│   ├── __init__.py          # Makes 'app' a Python package
│   ├── config.py            # Pydantic Settings for env variables
│   ├── database.py          # SQLAlchemy engine + session factory
│   ├── main.py              # FastAPI app creation + router registration
│   ├── middleware.py         # CORS, request logging, error handling
│   ├── models/              # SQLAlchemy ORM models (database tables)
│   │   ├── user.py          # User table: id, name, email, password, profile
│   │   ├── book.py          # Book table: title, price, condition, category
│   │   └── resource.py      # Resource table: title, file_path, type, tags
│   ├── schemas/             # Pydantic schemas (request/response validation)
│   │   ├── user.py          # UserCreate, UserResponse, LoginRequest
│   │   ├── book.py          # BookCreate, BookUpdate, BookResponse
│   │   └── resource.py      # ResourceCreate, ResourceResponse
│   ├── routers/             # API endpoint handlers (controllers)
│   │   ├── auth.py          # POST /auth/register, POST /auth/login
│   │   ├── users.py         # GET/PUT /users/me, GET /users/{id}
│   │   ├── books.py         # Full CRUD for book marketplace
│   │   └── resources.py     # Upload, browse, download resources
│   ├── services/            # Business logic layer
│   │   ├── auth_service.py  # Password hashing + JWT token management
│   │   └── file_service.py  # File upload, storage, deletion
│   └── utils/
│       └── dependencies.py  # Shared FastAPI dependencies (get_current_user)
├── frontend/                # Static frontend
│   ├── index.html           # Single-page HTML with all sections
│   ├── styles.css           # Dark theme design system
│   └── app.js               # Frontend logic (API calls, DOM manipulation)
├── tests/                   # Automated test suite
│   ├── conftest.py          # Test fixtures + isolated test database
│   ├── test_auth.py         # Registration + login tests
│   ├── test_books.py        # Book CRUD tests
│   └── test_resources.py    # Resource upload/download tests
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container build instructions
├── docker-compose.yml       # Multi-container orchestration
└── .env                     # Environment variables (SECRET_KEY, etc.)
```

### Design Patterns Used:

| Pattern | Where | Why |
|---------|-------|-----|
| **MVC (Model-View-Controller)** | models/ → schemas/ → routers/ | Separation of concerns |
| **Service Layer** | services/ | Business logic isolated from routes |
| **Dependency Injection** | `Depends()` in FastAPI | Loose coupling, testability |
| **Repository Pattern** | SQLAlchemy queries in routers | Database access abstraction |
| **Factory Pattern** | `get_settings()` with `@lru_cache` | Single config instance |
| **Singleton** | `@lru_cache()` on settings | Prevents re-reading .env per request |

---

## 🔄 4. Technology Choices — "Why X, Not Y?"

### ❓ Why **FastAPI** instead of Flask or Django?

| Factor | FastAPI ✅ | Flask ❌ | Django ❌ |
|--------|-----------|---------|----------|
| **Performance** | Async, built on Starlette (one of fastest Python frameworks) | Synchronous, slower | Heavy, slower |
| **Type Safety** | Built-in Pydantic validation | Manual validation needed | Has forms, but less modern |
| **Auto Docs** | Swagger UI + ReDoc auto-generated | Needs flask-swagger | Needs django-rest-framework |
| **Learning Curve** | Modern, Pythonic | Simple but bare-bones | Steep, opinionated |
| **Async Support** | Native async/await | Needs extensions | Limited |

**Interview Answer:**
> "I chose FastAPI because it provides automatic request/response validation via Pydantic, auto-generates interactive API docs (Swagger), has native async support, and is one of the fastest Python web frameworks. Flask would require manual validation and extra libraries for docs, while Django is too heavy for a focused API project."

---

### ❓ Why **SQLAlchemy** instead of raw SQL or MongoDB?

| Factor | SQLAlchemy ✅ | Raw SQL ❌ | MongoDB ❌ |
|--------|-------------|----------|-----------|
| **ORM** | Maps Python classes to tables | Manual queries | Different paradigm entirely |
| **SQL Injection** | Parameterized by default | Manual sanitization | N/A |
| **Relationships** | `relationship()` auto-joins | Manual JOINs | No joins (denormalized) |
| **Migrations** | Alembic support | Manual ALTER TABLE | Schema-less |
| **Type Safety** | Column types enforced | No compile-time checks | Schema-less |

**Interview Answer:**
> "SQLAlchemy provides an ORM that maps Python classes to database tables, preventing SQL injection by default, and enables easy relationship management with `relationship()`. Raw SQL would be error-prone and insecure, while MongoDB doesn't support the relational data model we need (users → books, users → resources)."

---

### ❓ Why **SQLite** instead of PostgreSQL or MySQL?

**Interview Answer:**
> "SQLite is perfect for development and small deployments — it's zero-config, file-based, and comes built into Python. The project is designed to be **easily swappable** to PostgreSQL by just changing the `DATABASE_URL` in `.env`. SQLAlchemy's ORM abstraction means no code changes are needed. For production, I would switch to PostgreSQL."

---

### ❓ Why **JWT** instead of session-based auth?

| Factor | JWT ✅ | Sessions ❌ |
|--------|-------|-----------|
| **Stateless** | No server-side session storage needed | Requires session store (Redis/DB) |
| **Scalable** | Works across multiple servers | Session affinity needed |
| **Frontend** | Simple `localStorage` + `Authorization` header | Cookie management |
| **API-friendly** | Standard for REST APIs | More suited for server-rendered apps |
| **Mobile-ready** | Easy to use in mobile apps | Cookie handling complex |

**Interview Answer:**
> "JWT is stateless — the server doesn't need to store sessions, making it horizontally scalable. The token is self-contained (holds user identity + expiry), and it's the standard for REST APIs. Session-based auth would require Redis or database session storage and doesn't work well with mobile clients."

---

### ❓ Why **bcrypt** instead of SHA-256 or MD5?

| Factor | bcrypt ✅ | SHA-256 ❌ | MD5 ❌ |
|--------|---------|----------|------|
| **Designed for passwords** | Yes, with work factor | No, it's a hash function | No |
| **Salt** | Automatic unique salt per hash | Manual salting needed | Manual salting needed |
| **Brute-force resistance** | Deliberately slow (configurable) | Fast (bad for passwords!) | Very fast (terrible!) |
| **Rainbow table resistant** | Yes (unique salt) | Vulnerable without salt | Vulnerable |

**Interview Answer:**
> "bcrypt is specifically designed for password hashing — it's deliberately slow (configurable cost factor) to resist brute-force attacks, automatically generates a unique salt per password, and is resistant to rainbow table attacks. SHA-256 and MD5 are fast hash functions designed for data integrity, not password security."

---

### ❓ Why **Pydantic** instead of Marshmallow or manual validation?

**Interview Answer:**
> "Pydantic v2 is deeply integrated with FastAPI — it automatically validates request bodies, query parameters, and generates OpenAPI schemas. It uses Python type hints (no extra schema definitions), runs validation in Rust (pydantic-core) for speed, and provides clear error messages. Marshmallow requires separate schema definitions and doesn't integrate with FastAPI's auto-documentation."

---

### ❓ Why **Vanilla JS** instead of React or Vue?

**Interview Answer:**
> "For this project, the frontend is relatively simple — a single-page app with 4 sections. Using React or Vue would add build tooling complexity (webpack/vite, node_modules, JSX transpilation) without much benefit. Vanilla JS keeps the frontend zero-dependency, fast-loading, and easy to understand. In a larger project, I would use React for component reusability and state management."

---

## 📦 5. Library-by-Library Explanation

### `requirements.txt` Breakdown:

```python
# ─── Core ──────────────────────────────────────────────
fastapi==0.115.0        # Web framework — handles routing, validation, docs
uvicorn==0.30.0         # ASGI server — runs the FastAPI app (like Gunicorn for Flask)
pydantic==2.9.0         # Data validation — validates request/response schemas
pydantic-settings==2.5.0 # Settings management — reads .env file into typed Python objects
email-validator==2.2.0  # Email validation — ensures valid email format in registration

# ─── Database ─────────────────────────────────────────
SQLAlchemy==2.0.35      # ORM — maps Python classes to database tables

# ─── Authentication ───────────────────────────────────
passlib[bcrypt]==1.7.4  # Password hashing library — provides CryptContext wrapper
python-jose[cryptography]==3.3.0  # JWT library — creates and verifies JSON Web Tokens
bcrypt==4.2.0           # bcrypt algorithm implementation — used by passlib

# ─── File Uploads ─────────────────────────────────────
python-multipart==0.0.12 # Parses multipart form data — required for file uploads

# ─── Environment ──────────────────────────────────────
python-dotenv==1.0.1    # Loads .env file — used by pydantic-settings

# ─── Testing ──────────────────────────────────────────
pytest==8.3.0           # Test framework — discovers and runs test functions
httpx==0.27.0           # Async HTTP client — used by FastAPI's TestClient
```

### Why each library exists:

| Library | Purpose | What happens if you remove it |
|---------|---------|-------------------------------|
| `fastapi` | The web framework | No API endpoints |
| `uvicorn` | ASGI server to run the app | App can't start |
| `pydantic` | Request validation | No input validation, raw dicts |
| `pydantic-settings` | Type-safe config | Manual `os.getenv()` calls |
| `email-validator` | Validates email format | Invalid emails accepted |
| `SQLAlchemy` | Database ORM | Manual SQL queries |
| `passlib[bcrypt]` | Password hashing | Plaintext passwords (insecure!) |
| `python-jose` | JWT tokens | No authentication |
| `python-multipart` | File uploads | Can't upload files |
| `python-dotenv` | `.env` loading | Hardcoded config values |
| `pytest` | Test runner | No automated tests |
| `httpx` | Test client HTTP | Tests can't make API calls |

---

## 🔍 6. File-by-File & Function-by-Function Walkthrough

### 📄 `app/config.py` — Application Configuration

```python
class Settings(BaseSettings):
    APP_NAME: str = "BookBridge API"        # App display name
    DATABASE_URL: str = "sqlite:///./bookbridge.db"  # DB connection string
    SECRET_KEY: str = "..."                 # JWT signing secret
    ALGORITHM: str = "HS256"                # JWT algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60   # Token lifespan
    UPLOAD_DIR: str = "uploads"             # File storage path
    MAX_FILE_SIZE_MB: int = 10              # Upload limit
    ALLOWED_ORIGINS: list[str] = [...]      # CORS whitelist

    class Config:
        env_file = ".env"                   # Auto-load from .env file
```

**Key concept:** `BaseSettings` from `pydantic-settings` automatically reads environment variables. The `class Config` with `env_file = ".env"` tells it to also check the `.env` file.

```python
@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

**`@lru_cache()`** — This decorator caches the function result. The `Settings()` object is created only ONCE and reused for all subsequent calls. Without this, every API request would re-read the `.env` file.

---

### 📄 `app/database.py` — Database Connection

```python
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite-specific
    pool_pre_ping=True,                         # Checks connection health
    echo=settings.DEBUG,                        # SQL logging in debug mode
)
```

**Why `check_same_thread=False`?**
> SQLite by default only allows one thread to access the database. FastAPI uses multiple threads (one per request). This flag disables that restriction.

**Why `pool_pre_ping=True`?**
> Before using a connection from the pool, SQLAlchemy pings the database to check if the connection is still alive. This prevents "connection closed" errors after the database restarts.

```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**`sessionmaker`** creates a factory that produces database sessions. Each session is a "unit of work" — you make changes and then `commit()` or `rollback()`.

```python
def get_db():
    db = SessionLocal()
    try:
        yield db        # Provide the session to the endpoint
    finally:
        db.close()      # Always close, even on errors
```

**This is a FastAPI Dependency** — the `yield` keyword makes it a context manager. The session is created before the endpoint runs and closed after.

---

### 📄 `app/services/auth_service.py` — Authentication Logic

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```
Creates a bcrypt hashing context. `deprecated="auto"` means if you later add a new scheme, old hashes will still work but new passwords will use the new scheme.

```python
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
    # Input:  "MyPassword123"
    # Output: "$2b$12$LJ3m4ys2Ien..." (60-char bcrypt hash)
```

```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
    # Extracts the salt from the hash, re-hashes the input, and compares
```

```python
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()                    # e.g. {"sub": "user@email.com"}
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})          # Add expiry to payload
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    # Output: "eyJhbGciOiJIUzI1NiIs..." (base64-encoded JWT string)
```

**JWT Structure:**
```
Header.Payload.Signature
  │       │        │
  │       │        └── HMAC-SHA256(header + payload, SECRET_KEY)
  │       └── {"sub": "user@email.com", "exp": 1709500000}
  └── {"alg": "HS256", "typ": "JWT"}
```

```python
def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload  # {"sub": "user@email.com", "exp": ...}
    except JWTError:
        return None     # Invalid or expired token
```

---

### 📄 `app/services/file_service.py` — File Upload Logic

```python
def save_upload_file(file: UploadFile, subfolder: str = "") -> tuple[str, str]:
    upload_dir = ensure_upload_dir()           # Create uploads/ if missing

    ext = os.path.splitext(file.filename)[1]   # Extract extension: ".pdf"
    unique_name = f"{uuid.uuid4().hex}{ext}"   # "a1b2c3d4e5f6.pdf"
    file_path = os.path.join(upload_dir, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)  # Stream file to disk

    return unique_name, file_path
```

**Why `uuid.uuid4().hex`?**
> Prevents filename collisions. Two users could upload `notes.pdf` — UUID ensures unique filenames. `uuid4()` generates a random UUID (not based on MAC address like `uuid1()`).

**Why `shutil.copyfileobj()`?**
> Streams the file in chunks instead of loading the entire file into memory. Essential for large files (10MB+).

---

### 📄 `app/middleware.py` — Cross-Cutting Concerns

```python
def setup_middleware(app: FastAPI) -> None:
    # CORS — allows frontend to call the API from a different origin
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,   # ["http://localhost:3000"]
        allow_credentials=True,
        allow_methods=["*"],                       # GET, POST, PUT, DELETE
        allow_headers=["*"],                       # Authorization, Content-Type
    )
```

**Why CORS is needed:**
> The frontend at `http://localhost:8000` (or `3000`) makes API calls to the backend. Browsers block **cross-origin requests** by default for security. CORS middleware adds `Access-Control-Allow-Origin` headers to tell the browser "this origin is allowed."

```python
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = round((time.time() - start_time) * 1000, 2)
        logger.info(f"{request.method} {request.url.path} → {response.status_code} ({duration}ms)")
        return response
```
Logs every HTTP request with method, path, status code, and timing. Example output:
```
2026-03-03 15:30:00 | INFO | bookbridge | GET /books → 200 (12.5ms)
```

```python
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
```
**Global error handler** — catches any unhandled exception and returns a clean 500 response instead of exposing stack traces to users.

---

### 📄 `app/models/book.py` — Book Database Model

```python
class BookCondition(str, enum.Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
```
**`str, enum.Enum`** — Inheriting from both `str` and `Enum` makes the enum JSON-serializable (FastAPI can return it as a string in responses).

```python
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)   # Auto-increment PK
    title = Column(String(300), index=True, nullable=False)  # Indexed for search
    price = Column(Float, nullable=False, default=0.0)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # FK to users table
    owner = relationship("User", back_populates="books")  # ORM relationship

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
```

**`index=True`** on `title` — Creates a B-tree index in the database, making `LIKE '%search%'` queries faster.

**`ForeignKey("users.id")`** — Creates a database-level constraint ensuring `owner_id` always references a valid user.

**`relationship("User", back_populates="books")`** — ORM-level relationship. Access `book.owner` to get the User object, or `user.books` to get all their books.

**`cascade="all, delete-orphan"`** — When a User is deleted, all their books are automatically deleted too.

---

### 📄 `app/routers/books.py` — Book API Endpoints

```python
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,                              # Pydantic validates request body
    db: Session = Depends(get_db),                 # Injected DB session
    current_user: User = Depends(get_current_user), # Injected authenticated user
):
```

**`Depends(get_current_user)`** — This is FastAPI's Dependency Injection. It:
1. Extracts the `Authorization: Bearer <token>` header
2. Decodes the JWT
3. Looks up the user in the database
4. Returns the User object (or raises 401)

```python
# Browse with filters and pagination
def browse_books(
    search: Optional[str] = Query(None),
    category: Optional[BookCategory] = Query(None),
    page: int = Query(1, ge=1),          # ge=1 means "must be ≥ 1"
    per_page: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(Book)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Book.title.ilike(search_term)) | (Book.author.ilike(search_term))
        )
    # ilike = case-insensitive LIKE
    # | = SQL OR operator
```

**Pagination logic:**
```python
    total = query.count()                    # COUNT(*) before pagination
    total_pages = math.ceil(total / per_page)
    books = query.order_by(Book.created_at.desc())  # Newest first
                 .offset((page - 1) * per_page)     # Skip previous pages
                 .limit(per_page)                    # Take only this page's items
                 .all()
```

---

### 📄 `app/routers/auth.py` — Authentication Endpoints

**Registration flow:**
```
Client → POST /auth/register {name, email, password}
  1. Check if email already exists → 409 Conflict
  2. Hash the password with bcrypt → "$2b$12$..."
  3. Create User record in database
  4. Return user info (without password)
```

**Login flow:**
```
Client → POST /auth/login {email, password}
  1. Find user by email → 401 if not found
  2. Verify password against bcrypt hash → 401 if wrong
  3. Create JWT token with {"sub": email, "exp": ...}
  4. Return {"access_token": "eyJ...", "token_type": "bearer"}
```

---

### 📄 `tests/conftest.py` — Test Setup

```python
TEST_DATABASE_URL = "sqlite:///./test_bookbridge.db"
test_engine = create_engine(TEST_DATABASE_URL, ...)

# Override the real database with test database
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)   # Create tables before each test
    yield
    Base.metadata.drop_all(bind=test_engine)     # Drop tables after each test
```

**Why `app.dependency_overrides`?**
> This is FastAPI's testing pattern. Instead of connecting to the real database, we replace the `get_db` dependency with one that connects to the test database. No code changes needed!

**Why `scope="function"` + `autouse=True`?**
> Each test function gets a fresh, empty database. `autouse=True` means this fixture runs automatically for every test without needing to be explicitly referenced.

---

## 🗄️ 7. Database Design & ORM Concepts

### Entity-Relationship Diagram:
```
┌─────────────┐        ┌─────────────────┐        ┌──────────────────┐
│    Users     │        │     Books       │        │   Resources      │
├─────────────┤        ├─────────────────┤        ├──────────────────┤
│ id (PK)     │◄───┐   │ id (PK)         │        │ id (PK)          │
│ name        │    ├──►│ owner_id (FK)   │        │ uploader_id (FK) │◄─┐
│ email (UQ)  │    │   │ title           │        │ title            │  │
│ password    │    │   │ author          │        │ file_name        │  │
│ college     │    │   │ price           │        │ file_path        │  │
│ year        │    │   │ condition       │        │ file_type        │  │
│ phone       │    │   │ category        │        │ category         │  │
│ bio         │    │   │ subject         │        │ subject          │  │
│ created_at  │    │   │ semester        │        │ tags             │  │
│ updated_at  │    │   │ is_available    │        │ download_count   │  │
└─────────────┘    │   │ created_at      │        │ created_at       │  │
                   │   │ updated_at      │        │ updated_at       │  │
                   │   └─────────────────┘        └──────────────────┘  │
                   │                                                    │
                   └────────────────────────────────────────────────────┘
                   One User → Many Books
                   One User → Many Resources
```

### Relationships:
- **User ↔ Books**: One-to-Many (a user can list many books)
- **User ↔ Resources**: One-to-Many (a user can upload many resources)
- **Cascade Delete**: Deleting a user automatically deletes all their books and resources

---

## 🔐 8. Authentication & Security Deep-Dive

### Complete Authentication Flow:

```
1. REGISTER:
   Client                           Server
   ──────                           ──────
   POST /auth/register ──────────►  Validate email uniqueness
   {name, email, password}          Hash password with bcrypt
                                    Store user in database
                          ◄──────── Return user info (201)

2. LOGIN:
   Client                           Server
   ──────                           ──────
   POST /auth/login ─────────────►  Find user by email
   {email, password}                Verify password vs bcrypt hash
                                    Create JWT: {sub: email, exp: ...}
                          ◄──────── Return {access_token: "eyJ...", token_type: "bearer"}

3. PROTECTED REQUEST:
   Client                           Server
   ──────                           ──────
   GET /books/my-listings ────────► Extract Bearer token from header
   Authorization: Bearer eyJ...     Decode JWT (verify signature + expiry)
                                    Look up user by email from JWT payload
                                    Execute the endpoint logic
                          ◄──────── Return protected data (200)
```

### Security Measures:

| Threat | Protection |
|--------|------------|
| **SQL Injection** | SQLAlchemy ORM parameterizes all queries |
| **Password Theft** | bcrypt hashing (passwords never stored in plain text) |
| **Token Forgery** | JWT signed with SECRET_KEY (HMAC-SHA256) |
| **Token Expiry** | Tokens expire after 60 minutes |
| **Cross-Origin Attacks** | CORS middleware restricts allowed origins |
| **Unauthorized Access** | `Depends(get_current_user)` on protected routes |
| **Privilege Escalation** | Owner checks (`book.owner_id != current_user.id`) |
| **File Upload Attacks** | UUID-based filenames prevent path traversal |
| **Sensitive Data Exposure** | `.env` file excluded from Git, passwords excluded from responses |

---

## 🌐 9. API Design & RESTful Principles

### RESTful Design Principles Applied:

| Principle | Example in BookBridge |
|-----------|----------------------|
| **Resource-based URLs** | `/books`, `/resources`, `/users` (nouns, not verbs) |
| **HTTP Methods = Actions** | GET=read, POST=create, PUT=update, DELETE=remove |
| **Status Codes** | 200=OK, 201=Created, 401=Unauthorized, 404=Not Found |
| **Stateless** | No server-side sessions, JWT in each request |
| **Pagination** | `?page=1&per_page=10` with total count in response |
| **Filtering** | Query params: `?category=engineering&condition=new` |
| **Consistent Response** | All endpoints return JSON with standard structure |

### API Endpoint Summary:

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | ❌ | Create account |
| POST | `/auth/login` | ❌ | Get JWT token |
| GET | `/users/me` | ✅ | My profile |
| PUT | `/users/me` | ✅ | Update profile |
| POST | `/books/` | ✅ | List a book for sale |
| GET | `/books/` | ❌ | Browse marketplace |
| GET | `/books/{id}` | ❌ | Book details |
| PUT | `/books/{id}` | ✅ | Update book (owner only) |
| DELETE | `/books/{id}` | ✅ | Delete book (owner only) |
| POST | `/resources/upload` | ✅ | Upload study resource |
| GET | `/resources/` | ❌ | Browse resources |
| GET | `/resources/{id}/download` | ❌ | Download file |
| DELETE | `/resources/{id}` | ✅ | Delete resource (owner only) |

---

## 🎨 10. Frontend Architecture

### Single-Page Application (SPA) Design:
The frontend is a **single HTML file** with multiple sections, toggled by JavaScript:

```javascript
function showSection(section) {
    // Hide all sections
    ['dashboardSection', 'buySection', 'sellSection', 'vaultSection']
        .forEach(id => document.getElementById(id).classList.add('hidden'));

    // Show the requested section
    document.getElementById(section + 'Section').classList.remove('hidden');

    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.dataset.section === section);
    });
}
```

### Key Frontend Patterns:

| Pattern | Implementation |
|---------|----------------|
| **Token Storage** | `localStorage.setItem('token', token)` |
| **API Helper** | `authHeaders()` adds `Authorization: Bearer <token>` |
| **Debounced Search** | Waits 300ms after user stops typing before calling API |
| **Toast Notifications** | Auto-dismissing success/error messages |
| **Modal System** | Overlay-based forms for create/edit operations |
| **Dynamic Rendering** | `innerHTML` with template strings to render cards |

### API Helper Functions:
```javascript
function authHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
    };
}

async function apiGet(path) {
    const res = await fetch(API_BASE + path, { headers: authHeaders() });
    if (!res.ok) throw await res.json();
    return res.json();
}
```

---

## 🧪 11. Testing Strategy

### Test Architecture:
```
tests/
├── conftest.py         # Shared fixtures (test DB, client, test user)
├── test_auth.py        # 5 tests: register, login, duplicate email, etc.
├── test_books.py       # 8 tests: CRUD, filters, authorization
└── test_resources.py   # 5 tests: upload, download, delete
```

### Key Testing Concepts:

1. **Dependency Override** — Replace real DB with test DB:
   ```python
   app.dependency_overrides[get_db] = override_get_db
   ```

2. **Fixture Chaining** — `auth_headers` depends on `test_user` depends on `client`:
   ```python
   @pytest.fixture
   def auth_headers(client, test_user):
       response = client.post("/auth/login", json={...})
       token = response.json()["access_token"]
       return {"Authorization": f"Bearer {token}"}
   ```

3. **Test Isolation** — Each test gets fresh tables (created before, dropped after).

4. **Example Test:**
   ```python
   def test_create_book(client, auth_headers):
       response = client.post("/books/", json={
           "title": "Engineering Mathematics",
           "author": "B.S. Grewal",
           "price": 250
       }, headers=auth_headers)
       assert response.status_code == 201
       assert response.json()["title"] == "Engineering Mathematics"
   ```

### Run Tests:
```bash
python -m pytest tests/ -v       # Verbose output
python -m pytest tests/ -v --tb=short  # Short tracebacks
```

---

## 🐳 12. DevOps & Deployment

### Dockerfile Explained:
```dockerfile
FROM python:3.12-slim          # Lightweight Python base image (~150MB vs ~1GB full)

WORKDIR /app                   # Set working directory inside container

RUN apt-get update && apt-get install -y gcc  # gcc needed to compile bcrypt

COPY requirements.txt .        # Copy deps first (Docker layer caching!)
RUN pip install --no-cache-dir -r requirements.txt  # Install Python packages

COPY . .                       # Copy all project files

RUN mkdir -p uploads           # Create uploads directory

EXPOSE 8000                    # Document the port

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Why copy `requirements.txt` separately?**
> Docker caches layers. If only your code changes (not requirements), Docker reuses the cached pip install layer — much faster rebuilds.

### Docker Commands:
```bash
docker build -t bookbridge .              # Build image
docker run -p 8000:8000 bookbridge        # Run container
docker-compose up                         # Run with docker-compose
```

---

## ❓ 13. Interview Q&A (30+ Questions)

### General Questions:

**Q1: Tell me about your project in 30 seconds.**
> "BookBridge is a full-stack web platform for college students to buy/sell second-hand academic books and share study resources. I built the backend with Python FastAPI, SQLAlchemy ORM, JWT authentication, and a vanilla HTML/CSS/JS frontend. Key features include search with filters, pagination, file uploads, role-based authorization, automated tests, and Docker deployment."

**Q2: What was the most challenging part?**
> "Implementing the authentication flow — ensuring JWT tokens are properly created, validated, and expired, while keeping the password hashing secure with bcrypt. I also had to handle edge cases like expired tokens, duplicate emails, and unauthorized access to other users' listings."

**Q3: If you had more time, what would you add?**
> "Real-time chat between buyers and sellers using WebSockets, image upload for book covers, payment integration (Razorpay), email verification with OTP, and a recommendation engine based on the user's college and semester."

---

### Backend Questions:

**Q4: What is FastAPI and why did you choose it?**
> "FastAPI is a modern Python web framework built on Starlette and Pydantic. I chose it for automatic request validation, auto-generated API documentation (Swagger), native async support, and excellent performance benchmarks."

**Q5: Explain Dependency Injection in FastAPI.**
> "FastAPI's `Depends()` function injects dependencies into endpoint functions. For example, `Depends(get_db)` creates a database session for each request and auto-closes it. `Depends(get_current_user)` extracts the JWT token, decodes it, and provides the authenticated user object. This makes endpoints declarative and testable."

**Q6: How does your database session management work?**
> "The `get_db()` function is a generator that creates a SQLAlchemy session, yields it to the endpoint, and closes it in the `finally` block — ensuring cleanup even on errors. It's used as a FastAPI dependency via `Depends(get_db)`."

**Q7: What is `@lru_cache()` and why did you use it on `get_settings()`?**
> "`@lru_cache()` is a Python decorator that caches function return values. I used it on `get_settings()` so the `.env` file is read only once at startup, not on every API request. It's a singleton pattern implementation."

**Q8: Explain the difference between models and schemas.**
> "Models (SQLAlchemy) define the database table structure — columns, types, relationships. Schemas (Pydantic) define the API contract — what the client sends and receives. For example, `BookCreate` schema has `title, author, price` for creating a book, but `BookResponse` schema includes `id, created_at, owner_id` which are generated by the database."

**Q9: How do you handle partial updates (PATCH/PUT)?**
> "I use Pydantic's `model_dump(exclude_unset=True)` which only returns fields that the client explicitly provided. This allows partial updates — the client can send `{"price": 300}` without having to re-send the entire book object."

**Q10: How do you prevent SQL injection?**
> "SQLAlchemy's ORM parameterizes all queries automatically. When I write `Book.title.ilike(f'%{search}%')`, SQLAlchemy generates a parameterized query like `WHERE title LIKE ?` with the search term as a separate parameter, not concatenated into the SQL string."

---

### Authentication Questions:

**Q11: Explain the JWT authentication flow step by step.**
> "1) User registers — password is hashed with bcrypt and stored. 2) User logs in — server verifies the password, creates a JWT with the user's email and expiry time, signs it with a secret key, and returns it. 3) For protected requests, the client sends the JWT in the `Authorization: Bearer <token>` header. 4) The server decodes the token, verifies the signature and expiry, looks up the user, and proceeds with the request."

**Q12: Why is bcrypt better than SHA-256 for passwords?**
> "bcrypt is deliberately slow (configurable cost factor), making brute-force attacks impractical. It automatically generates a unique salt per password, preventing rainbow table attacks. SHA-256 is a fast hash designed for data integrity — it can hash billions of passwords per second, making it vulnerable to brute-force."

**Q13: What happens when a JWT expires?**
> "The `python-jose` library checks the `exp` claim during decoding. If the current time is past the expiry, `jwt.decode()` raises a `JWTError`, which our `decode_access_token()` catches and returns `None`. The `get_current_user` dependency then raises a 401 Unauthorized response."

**Q14: How do you protect against unauthorized access to resources?**
> "Two levels: 1) **Authentication** — `Depends(get_current_user)` ensures only logged-in users can access protected endpoints. 2) **Authorization** — In update/delete endpoints, I check `if book.owner_id != current_user.id` and raise 403 Forbidden if the user isn't the owner."

---

### Database Questions:

**Q15: Explain the One-to-Many relationship between User and Book.**
> "In the database, `books` table has an `owner_id` column as a foreign key referencing `users.id`. In SQLAlchemy, the `User` model has `books = relationship('Book', back_populates='owner')` and `Book` has `owner = relationship('User', back_populates='books')`. This creates bidirectional navigation — `user.books` returns all books, `book.owner` returns the user."

**Q16: What is cascade delete and why is it important?**
> "I set `cascade='all, delete-orphan'` on the User → Books relationship. When a user is deleted, all their books are automatically deleted too. Without this, you'd get orphan records (books with no owner) or foreign key constraint errors."

**Q17: Why did you use SQLite and how would you switch to PostgreSQL?**
> "SQLite for development — zero configuration, single file. To switch, I just change `DATABASE_URL` in `.env` from `sqlite:///./bookbridge.db` to `postgresql://user:password@host/dbname`. SQLAlchemy's ORM abstraction means zero code changes."

**Q18: What is `pool_pre_ping` and why is it needed?**
> "It's a connection pool health check. Before using a connection from the pool, SQLAlchemy pings the database. If the connection is stale (e.g., database restarted), it's recycled. This prevents 'connection closed' errors in production."

---

### Frontend Questions:

**Q19: How do you store the JWT token on the frontend?**
> "In `localStorage`. After login, `localStorage.setItem('token', token)`. For every API call, `authHeaders()` reads it and adds `Authorization: Bearer <token>`. On logout, `localStorage.removeItem('token')` clears it."

**Q20: What is debouncing and why do you use it for search?**
> "Debouncing delays a function call until the user stops triggering it. For the search input, instead of calling the API on every keystroke ('E', 'En', 'Eng'...), I wait 300ms after the last keystroke. This reduces unnecessary API calls from ~20 to ~1 per search."

**Q21: Why did you use vanilla JavaScript instead of React?**
> "The frontend has ~4 views and straightforward DOM manipulation. React's component model, virtual DOM, and build tooling (webpack/vite) would add complexity without significant benefit. For a larger app with 20+ components or shared state, I'd absolutely use React."

---

### Testing Questions:

**Q22: How do you isolate tests from the production database?**
> "FastAPI's `dependency_overrides` feature. I override `get_db` to return a session connected to a test SQLite database. Each test creates fresh tables (`create_all`) and drops them after (`drop_all`), ensuring complete isolation."

**Q23: What is a pytest fixture?**
> "A fixture is a reusable setup function. For example, `test_user` fixture registers a user and returns credentials. `auth_headers` fixture logs in and returns the JWT header. Fixtures can depend on each other — `auth_headers` depends on `test_user` which depends on `client`."

**Q24: How do you test protected endpoints?**
> "I use the `auth_headers` fixture which automatically registers a user, logs in, and returns `{'Authorization': 'Bearer <token>'}`. I pass these headers to the test client: `client.post('/books/', json={...}, headers=auth_headers)`."

---

### Architecture & Design Questions:

**Q25: What design patterns did you use?**
> "MVC (models/schemas/routers), Service Layer (auth_service, file_service), Dependency Injection (FastAPI's `Depends`), Factory/Singleton (`@lru_cache` for settings), and Repository Pattern (SQLAlchemy queries)."

**Q26: How would you scale this for 10,000 users?**
> "1) Switch SQLite to PostgreSQL. 2) Add Redis for caching frequent queries. 3) Use Nginx as a reverse proxy. 4) Deploy multiple app instances behind a load balancer. 5) Move file uploads to AWS S3 or Cloudinary. 6) Add database connection pooling with PgBouncer."

**Q27: How do you handle errors globally?**
> "The `global_exception_handler` in middleware catches any unhandled exception, logs the full traceback for debugging, and returns a clean `500 Internal Server Error` response. This prevents stack traces from leaking to users."

**Q28: What is CORS and why do you need it?**
> "CORS (Cross-Origin Resource Sharing) is a browser security feature. When the frontend on `localhost:8000` makes API calls to the backend, the browser checks if the server allows this origin. My CORS middleware adds the `Access-Control-Allow-Origin` header to permit cross-origin requests."

---

### Scenario-Based Questions:

**Q29: A user reports they can edit other users' books. How do you debug?**
> "1) Check the `update_book` endpoint for the owner check: `if book.owner_id != current_user.id`. 2) Verify `get_current_user` correctly extracts the user from JWT. 3) Write a test case that attempts edit with a different user's token and asserts 403. 4) Check if the frontend is sending the correct Authorization header."

**Q30: How would you add password reset functionality?**
> "1) Add a `/auth/forgot-password` endpoint that generates a time-limited reset token and sends it via email. 2) Add `/auth/reset-password` that accepts the token and new password. 3) Store reset tokens in the database with an expiry timestamp. 4) Validate the token hasn't expired before allowing the password change."

**Q31: What if two users upload a file with the same name?**
> "No collision — `file_service.py` generates a UUID-based filename for every upload: `uuid.uuid4().hex + extension`. Two `notes.pdf` uploads become `a1b2c3d4.pdf` and `e5f6g7h8.pdf`."

**Q32: How would you add rate limiting?**
> "Use `slowapi` library (built for FastAPI) with a decorator like `@limiter.limit('10/minute')`. Configure different limits for different endpoints — stricter for `/auth/login` (prevent brute force), lenient for `/books/` (browsing)."

**Q33: How would you implement image uploads for book covers?**
> "1) Extend `file_service.py` to validate image types (JPEG, PNG). 2) Add `image_url` field (already in the Book model). 3) Create a `/books/{id}/upload-image` endpoint that saves the image and updates the book record. 4) Serve images as static files via FastAPI's `StaticFiles` mount."

---

### DevOps Questions:

**Q34: Explain your Dockerfile line by line.**
> *"(See Section 12 — DevOps & Deployment for the full explanation)"*

**Q35: Why do you copy `requirements.txt` before the rest of the code?**
> "Docker layer caching. If I change Python code but not dependencies, Docker reuses the cached `pip install` layer instead of re-installing all packages. This makes rebuilds much faster (seconds instead of minutes)."

---

## 🎓 Quick Reference Card

### One-Line Descriptions for Every File:

| File | One-Line Description |
|------|---------------------|
| `config.py` | Loads environment variables into type-safe Settings object |
| `database.py` | Creates SQLAlchemy engine, session factory, and DB dependency |
| `main.py` | FastAPI app factory — registers routers, middleware, and mounts frontend |
| `middleware.py` | Configures CORS, request logging, and global error handling |
| `models/user.py` | User database table with profile fields and relationships |
| `models/book.py` | Book database table with enums for condition and category |
| `models/resource.py` | Resource database table with file metadata and download counter |
| `schemas/user.py` | Pydantic models for user registration, login, and response |
| `schemas/book.py` | Pydantic models for book create, update, and list response |
| `schemas/resource.py` | Pydantic models for resource create and response |
| `routers/auth.py` | Registration and login endpoints |
| `routers/users.py` | User profile endpoints (view, update) |
| `routers/books.py` | Full CRUD + search/filter/pagination for book marketplace |
| `routers/resources.py` | Upload, browse, download, and delete study resources |
| `services/auth_service.py` | bcrypt password hashing + JWT creation/verification |
| `services/file_service.py` | UUID-based file upload, storage, and deletion |
| `utils/dependencies.py` | `get_current_user` dependency for protected routes |
| `conftest.py` | Test fixtures — isolated test DB, test client, test user |
| `Dockerfile` | Container build instructions with layer caching |

---

*Last updated: March 2026*
