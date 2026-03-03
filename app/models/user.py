"""
User model — stores registered users with profile information.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Profile fields
    college = Column(String(200), default="")
    year = Column(String(20), default="")       # e.g. "3rd Year", "Alumni"
    phone = Column(String(20), default="")
    bio = Column(Text, default="")

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    books = relationship("Book", back_populates="owner", cascade="all, delete-orphan")
    resources = relationship("Resource", back_populates="uploader", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
