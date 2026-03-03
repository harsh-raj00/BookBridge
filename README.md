# 📚 BookBridge

**BookBridge** is a full-stack platform where college students can **buy/sell academic books** and **share study resources** (notes, PDFs, assignments) — all in one centralized system.

> Built with **Python (FastAPI)**, **SQLAlchemy**, **JWT Auth**, and a **vanilla HTML/CSS/JS** frontend.

---

## 🚀 Features

### 📖 Book Marketplace
- List books for sale with **price, condition, category**
- Browse with **search, filters** (category, condition, price range)
- Full **CRUD operations** with owner authorization
- Categories: Engineering, Medical, Competitive, School, Arts, Science, Commerce, Law

### 📝 StudyVault (Resource Sharing)
- Upload & share **notes, PDFs, assignments, question papers**
- Filter by **type, subject, semester**
- **Download counter** tracking
- Tag-based organization

### 🔐 Authentication
- JWT-based authentication with **bcrypt** password hashing
- Protected routes with **Bearer token** authorization
- User profiles with college, year, bio

---

## 🏗️ Architecture

```
BookBridge/
├── app/                          # Backend (FastAPI)
│   ├── config.py                 # Pydantic Settings
│   ├── database.py               # SQLAlchemy engine & session
│   ├── main.py                   # App entry point
│   ├── middleware.py              # CORS, logging, error handling
│   ├── models/                   # SQLAlchemy models
│   │   ├── user.py               # User model
│   │   ├── book.py               # Book model + enums
│   │   └── resource.py           # Resource model + enums
│   ├── schemas/                  # Pydantic schemas
│   │   ├── user.py
│   │   ├── book.py
│   │   └── resource.py
│   ├── routers/                  # API route handlers
│   │   ├── auth.py               # Registration & login
│   │   ├── users.py              # Profile management
│   │   ├── books.py              # Book CRUD + marketplace
│   │   └── resources.py          # StudyVault upload/download
│   ├── services/                 # Business logic
│   │   ├── auth_service.py       # JWT & password hashing
│   │   └── file_service.py       # File upload/storage
│   └── utils/
│       └── dependencies.py       # Shared FastAPI dependencies
├── frontend/                     # Frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/                        # Test suite
│   ├── conftest.py               # Fixtures & test DB
│   ├── test_auth.py
│   ├── test_books.py
│   └── test_resources.py
├── uploads/                      # File storage
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## ⚡ Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/BookBridge.git
cd BookBridge
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and set a strong SECRET_KEY
```

### 3. Run Server
```bash
uvicorn app.main:app --reload
```

### 4. Access
- **Frontend**: http://127.0.0.1:8000/frontend/index.html
- **API Docs (Swagger)**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 🧪 Testing

```bash
python -m pytest tests/ -v
```

---

## 📡 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register new user | ❌ |
| POST | `/auth/login` | Login & get JWT | ❌ |
| GET | `/users/me` | My profile | ✅ |
| PUT | `/users/me` | Update profile | ✅ |
| GET | `/users/{id}` | View user profile | ❌ |
| POST | `/books/` | List a book | ✅ |
| GET | `/books/` | Browse marketplace | ❌ |
| GET | `/books/{id}` | Book details | ❌ |
| PUT | `/books/{id}` | Update listing | ✅ |
| DELETE | `/books/{id}` | Delete listing | ✅ |
| GET | `/books/my-listings` | My books | ✅ |
| GET | `/books/categories` | Categories list | ❌ |
| POST | `/resources/upload` | Upload resource | ✅ |
| GET | `/resources/` | Browse resources | ❌ |
| GET | `/resources/{id}` | Resource details | ❌ |
| GET | `/resources/{id}/download` | Download file | ❌ |
| DELETE | `/resources/{id}` | Delete resource | ✅ |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.12, FastAPI |
| **ORM** | SQLAlchemy 2.0 |
| **Database** | SQLite (swappable to PostgreSQL) |
| **Auth** | JWT (python-jose) + bcrypt |
| **Validation** | Pydantic v2 |
| **Frontend** | Vanilla HTML/CSS/JS |
| **Testing** | pytest + httpx |

---

## 📄 License

MIT License
