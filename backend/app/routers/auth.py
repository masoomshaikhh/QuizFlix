
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.schemas.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse
)
from backend.app.services.auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    # Check password length before bcrypt hashing
    if len(user_data.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must not exceed 72 bytes."
        )

    # Check whether email already exists
    existing_email = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=409,
            detail="Email already registered."
        )

    # Check whether username already exists
    existing_username = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=409,
            detail="Username already taken."
        )

    # Hash password before saving
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role="user"
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists."
        )

    return new_user


@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    # Find user using email
    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    # Verify password
    if not user or not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Generate JWT token
    access_token = create_access_token(user.user_id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
