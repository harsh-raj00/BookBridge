"""
Books router — full CRUD for the book marketplace.

Endpoints:
    POST   /books              - Create a book listing
    GET    /books              - Browse marketplace with filters & pagination
    GET    /books/categories   - List available categories
    GET    /books/my-listings  - Get current user's listed books
    GET    /books/{book_id}    - Get book details
    PUT    /books/{book_id}    - Update a book listing (owner only)
    DELETE /books/{book_id}    - Delete a book listing (owner only)
"""

import math
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models.book import Book, BookCondition, BookCategory
from ..models.user import User
from ..schemas.book import BookCreate, BookUpdate, BookResponse, BookListResponse
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new book listing on the marketplace.
    The authenticated user becomes the owner/seller.
    """
    new_book = Book(
        title=book.title,
        author=book.author,
        description=book.description,
        isbn=book.isbn,
        edition=book.edition,
        price=book.price,
        condition=book.condition,
        category=book.category,
        subject=book.subject,
        semester=book.semester,
        image_url=book.image_url,
        owner_id=current_user.id,
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@router.get("/categories")
def get_categories():
    """List all available book categories and conditions."""
    return {
        "categories": [c.value for c in BookCategory],
        "conditions": [c.value for c in BookCondition],
    }


@router.get("/my-listings", response_model=list[BookResponse])
def get_my_listings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all books listed by the authenticated user."""
    books = db.query(Book).filter(Book.owner_id == current_user.id).all()
    return books


@router.get("/", response_model=BookListResponse)
def browse_books(
    search: Optional[str] = Query(None, description="Search in title or author"),
    category: Optional[BookCategory] = Query(None, description="Filter by category"),
    condition: Optional[BookCondition] = Query(None, description="Filter by condition"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    available_only: bool = Query(True, description="Show only available books"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=50, description="Items per page"),
    db: Session = Depends(get_db),
):
    """
    Browse the book marketplace with filters and pagination.

    Supports:
    - Full-text search in title and author
    - Category, condition, subject filters
    - Price range filtering
    - Pagination with metadata
    """
    query = db.query(Book)

    # Apply filters
    if available_only:
        query = query.filter(Book.is_available == True)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Book.title.ilike(search_term)) | (Book.author.ilike(search_term))
        )

    if category:
        query = query.filter(Book.category == category)

    if condition:
        query = query.filter(Book.condition == condition)

    if min_price is not None:
        query = query.filter(Book.price >= min_price)

    if max_price is not None:
        query = query.filter(Book.price <= max_price)

    if subject:
        query = query.filter(Book.subject.ilike(f"%{subject}%"))

    # Count total before pagination
    total = query.count()
    total_pages = math.ceil(total / per_page) if total > 0 else 1

    # Apply pagination and order by newest first
    books = query.order_by(Book.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return BookListResponse(
        books=books,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
    )


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get details of a specific book."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    updates: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a book listing. Only the owner can update.
    Supports partial updates — only provided fields are changed.
    """
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    if book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this book")

    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)

    return book


@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a book listing. Only the owner can delete.
    Permanently removes the listing from the marketplace.
    """
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    if book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this book")

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully", "book_id": book_id}
