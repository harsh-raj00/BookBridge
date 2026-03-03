"""
Book model — represents a book listing in the marketplace.
Supports pricing, condition grading, and category-based filtering.
"""

import enum
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..database import Base


class BookCondition(str, enum.Enum):
    """Condition grading for second-hand books."""
    NEW = "new"
    LIKE_NEW = "like_new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class BookCategory(str, enum.Enum):
    """Academic categories for book classification."""
    ENGINEERING = "engineering"
    MEDICAL = "medical"
    COMPETITIVE = "competitive"
    SCHOOL = "school"
    ARTS = "arts"
    SCIENCE = "science"
    COMMERCE = "commerce"
    LAW = "law"
    OTHER = "other"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)

    # Core book info
    title = Column(String(300), index=True, nullable=False)
    author = Column(String(200), nullable=False)
    description = Column(Text, default="")
    isbn = Column(String(20), default="")
    edition = Column(String(50), default="")

    # Marketplace fields
    price = Column(Float, nullable=False, default=0.0)
    condition = Column(Enum(BookCondition), default=BookCondition.GOOD)
    category = Column(Enum(BookCategory), default=BookCategory.OTHER)
    subject = Column(String(200), default="")
    semester = Column(String(20), default="")

    # Availability
    is_available = Column(Boolean, default=True, index=True)
    image_url = Column(String(500), default="")

    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    owner = relationship("User", back_populates="books")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', price={self.price})>"
