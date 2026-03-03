"""
Resources router — StudyVault: upload, browse, and download study resources.

Endpoints:
    POST   /resources/upload      - Upload a study resource (notes, PDF, etc.)
    GET    /resources              - Browse resources with filters & pagination
    GET    /resources/my-uploads   - Get current user's uploaded resources
    GET    /resources/{id}         - Get resource details
    GET    /resources/{id}/download - Download the resource file
    DELETE /resources/{id}         - Delete a resource (owner only)
"""

import math
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models.resource import Resource, ResourceType
from ..models.user import User
from ..schemas.resource import ResourceResponse, ResourceListResponse
from ..services.file_service import save_upload_file, delete_file
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/resources", tags=["Resources (StudyVault)"])


@router.post("/upload", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
def upload_resource(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(""),
    file_type: ResourceType = Form(ResourceType.OTHER),
    category: str = Form(""),
    subject: str = Form(""),
    semester: str = Form(""),
    tags: str = Form(""),
    is_public: bool = Form(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a study resource (notes, PDF, assignment, etc.).

    The file is stored on disk and metadata is saved to the database.
    Uses Form fields (not JSON body) since we're uploading a file.
    """
    # Save file to disk
    saved_name, file_path = save_upload_file(file, subfolder="resources")

    # Save metadata to DB
    resource = Resource(
        title=title,
        description=description,
        file_name=file.filename or saved_name,
        file_path=file_path,
        file_type=file_type,
        category=category,
        subject=subject,
        semester=semester,
        tags=tags,
        is_public=is_public,
        uploader_id=current_user.id,
    )

    db.add(resource)
    db.commit()
    db.refresh(resource)

    return resource


@router.get("/my-uploads", response_model=list[ResourceResponse])
def get_my_uploads(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all resources uploaded by the authenticated user."""
    resources = db.query(Resource).filter(Resource.uploader_id == current_user.id).all()
    return resources


@router.get("/", response_model=ResourceListResponse)
def browse_resources(
    search: Optional[str] = Query(None, description="Search in title or description"),
    file_type: Optional[ResourceType] = Query(None, description="Filter by resource type"),
    category: Optional[str] = Query(None, description="Filter by category"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    semester: Optional[str] = Query(None, description="Filter by semester"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=50, description="Items per page"),
    db: Session = Depends(get_db),
):
    """
    Browse study resources with filters and pagination.
    Only public resources are shown.
    """
    query = db.query(Resource).filter(Resource.is_public == True)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Resource.title.ilike(search_term)) | (Resource.description.ilike(search_term))
        )

    if file_type:
        query = query.filter(Resource.file_type == file_type)

    if category:
        query = query.filter(Resource.category.ilike(f"%{category}%"))

    if subject:
        query = query.filter(Resource.subject.ilike(f"%{subject}%"))

    if semester:
        query = query.filter(Resource.semester == semester)

    # Count total
    total = query.count()
    total_pages = math.ceil(total / per_page) if total > 0 else 1

    # Paginate, newest first
    resources = query.order_by(Resource.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return ResourceListResponse(
        resources=resources,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
    )


@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    """Get details of a specific resource."""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return resource


@router.get("/{resource_id}/download")
def download_resource(resource_id: int, db: Session = Depends(get_db)):
    """
    Download a resource file.
    Increments the download counter on each access.
    """
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    # Increment download count
    resource.download_count += 1
    db.commit()

    return FileResponse(
        path=resource.file_path,
        filename=resource.file_name,
        media_type="application/octet-stream",
    )


@router.delete("/{resource_id}", status_code=status.HTTP_200_OK)
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a resource. Only the uploader can delete.
    Removes both the file from disk and the database record.
    """
    resource = db.query(Resource).filter(Resource.id == resource_id).first()

    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    if resource.uploader_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this resource")

    # Delete file from disk
    delete_file(resource.file_path)

    # Delete from DB
    db.delete(resource)
    db.commit()

    return {"message": "Resource deleted successfully", "resource_id": resource_id}
