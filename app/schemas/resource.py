"""
Resource schemas — request/response validation for StudyVault endpoints.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from ..models.resource import ResourceType


class ResourceCreate(BaseModel):
    """Schema for creating a resource (metadata only — file sent separately)."""
    title: str
    description: str = ""
    file_type: ResourceType = ResourceType.OTHER
    category: str = ""
    subject: str = ""
    semester: str = ""
    tags: str = ""
    is_public: bool = True


class ResourceResponse(BaseModel):
    """Schema for a single resource response."""
    id: int
    title: str
    description: str
    file_name: str
    file_type: ResourceType
    category: str
    subject: str
    semester: str
    tags: str
    download_count: int
    is_public: bool
    uploader_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ResourceListResponse(BaseModel):
    """Schema for paginated resource list response."""
    resources: list[ResourceResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
