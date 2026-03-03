

from .database import engine, Base
from . import models

from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import UserCreate, UserResponse


from fastapi import HTTPException
from .auth import verify_password, create_access_token
from .auth import hash_password
from .schemas import LoginRequest
from .auth import get_current_user
from .models import User


Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
app = FastAPI(title="BookBridge API")


@app.get("/")
def root():
    return {"message": "Welcome to the BookBridge and Backend Running!"}

from .models import User

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "message": "Authorized access",
        "email": current_user.email
    }