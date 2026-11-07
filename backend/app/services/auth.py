from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import jwt

from ..config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """Hash a user's password."""
    if not password:
        raise ValueError("Password cannot be empty.")

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its stored hash."""
    if not plain_password or not hashed_password:
        return False

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    """Generate a JWT access token for a user."""

    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not configured.")

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token