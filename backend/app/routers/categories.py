

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.category import Category
from backend.app.models.question import Question
from backend.app.models.user import User
from backend.app.services.dependencies import get_admin_user
from backend.app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate
)


router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"]
)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    existing_category = db.query(Category).filter(
        Category.category_name == category_data.category_name
    ).first()

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists."
        )

    new_category = Category(
        category_name=category_data.category_name,
        description=category_data.description
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get(
    "/",
    response_model=list[CategoryResponse]
)
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.category_id).all()


@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.category_id == category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found."
        )

    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    category = db.query(Category).filter(
        Category.category_id == category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found."
        )

    update_data = category_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No update information provided."
        )

    if "category_name" in update_data:
        existing = db.query(Category).filter(
            Category.category_name == update_data["category_name"],
            Category.category_id != category_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Category name already exists."
            )

    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    category = db.query(Category).filter(
        Category.category_id == category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found."
        )

    existing_questions = db.query(Question).filter(
        Question.category_id == category_id
    ).first()

    if existing_questions:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete a category that contains questions."
        )

    db.delete(category)
    db.commit()

    return {
        "message": "Category deleted successfully."
    }
