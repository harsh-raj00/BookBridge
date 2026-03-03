"""
Resource model — represents a shared study resource (notes, PDFs, assignments).
Part of the StudyVault feature for academic resource sharing.
"""

import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..database import Base


class ResourceType(str, enum.Enum):
    """Type of study resource."""
    NOTES = "notes"
    PDF = "pdf"
    ASSIGNMENT = "assignment"
    QUESTION_PAPER = "question_paper"
    SOLUTION = "solution"
    PRESENTATION = "presentation"
    OTHER = "other"


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)

    # Resource metadata
    title = Column(String(300), index=True, nullable=False)
    description = Column(Text, default="")
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(Enum(ResourceType), default=ResourceType.OTHER)

    # Academic classification
    category = Column(String(100), default="")     # e.g. "Engineering", "Medical"
    subject = Column(String(200), default="")
    semester = Column(String(20), default="")
    tags = Column(String(500), default="")          # comma-separated tags

    # Engagement
    download_count = Column(Integer, default=0)
    is_public = Column(Boolean, default=True, index=True)

    # Foreign keys
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    uploader = relationship("User", back_populates="resources")

    def __repr__(self):
        return f"<Resource(id={self.id}, title='{self.title}')>"
