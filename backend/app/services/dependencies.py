
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.config import SECRET_KEY, ALGORITHM
from backend.app.models.user import User

security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    print("AUTHENTICATION CHECK STARTED")

    if credentials is None:
        print("No bearer token received")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token missing."
        )

    token = credentials.credentials
    print("Bearer token received:", bool(token))

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("JWT decoded successfully")
        print("JWT payload:", payload)

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="User ID missing from token."
            )

    except JWTError as error:
        print("JWT DECODING ERROR:", str(error))
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    user = db.query(User).filter(
        User.user_id == int(user_id)
    ).first()

    print("DATABASE USER FOUND:", user is not None)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found."
        )

    return user


def get_admin_user(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required."
        )

    return current_user
