"""
Book schemas — request/response validation for book marketplace endpoints.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from ..models.book import BookCondition, BookCategory


class BookCreate(BaseModel):
    """Schema for creating a book listing."""
    title: str
    author: str
    description: str = ""
    isbn: str = ""
    edition: str = ""
    price: float
    condition: BookCondition = BookCondition.GOOD
    category: BookCategory = BookCategory.OTHER
    subject: str = ""
    semester: str = ""
    image_url: str = ""


class BookUpdate(BaseModel):
    """Schema for updating a book listing. All fields optional."""
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None
    edition: Optional[str] = None
    price: Optional[float] = None
    condition: Optional[BookCondition] = None
    category: Optional[BookCategory] = None
    subject: Optional[str] = None
    semester: Optional[str] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None


class BookResponse(BaseModel):
    """Schema for a single book response."""
    id: int
    title: str
    author: str
    description: str
    isbn: str
    edition: str
    price: float
    condition: BookCondition
    category: BookCategory
    subject: str
    semester: str
    is_available: bool
    image_url: str
    owner_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BookListResponse(BaseModel):
    """Schema for paginated book list response."""
    books: list[BookResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
