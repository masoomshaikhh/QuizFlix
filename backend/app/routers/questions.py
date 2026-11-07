
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.category import Category
from backend.app.models.question import Question
from backend.app.schemas.question import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate
)
from backend.app.services.dependencies import get_admin_user
from backend.app.models.user import User


router = APIRouter(
    prefix="/api/questions",
    tags=["Questions"]
)


@router.post(
    "/",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    category = db.query(Category).filter(
        Category.category_id == question_data.category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found."
        )

    new_question = Question(
        category_id=question_data.category_id,
        question_text=question_data.question_text,
        difficulty=question_data.difficulty,
        explanation=question_data.explanation
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question


@router.get(
    "/",
    response_model=list[QuestionResponse]
)
def get_questions(
    category_id: int | None = None,
    difficulty: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Question)

    if category_id is not None:
        query = query.filter(Question.category_id == category_id)

    if difficulty is not None:
        if difficulty not in ["Easy", "Medium", "Hard"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Difficulty must be Easy, Medium or Hard."
            )
        query = query.filter(Question.difficulty == difficulty)

    return query.order_by(Question.question_id).all()


@router.get(
    "/{question_id}",
    response_model=QuestionResponse
)
def get_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(
        Question.question_id == question_id
    ).first()

    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found."
        )

    return question


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    question = db.query(Question).filter(
        Question.question_id == question_id
    ).first()

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )

    update_data = question_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No update information provided."
        )

    if "category_id" in update_data:
        category = db.query(Category).filter(
            Category.category_id == update_data["category_id"]
        ).first()

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found."
            )

    for key, value in update_data.items():
        setattr(question, key, value)

    db.commit()
    db.refresh(question)

    return question


@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    question = db.query(Question).filter(
        Question.question_id == question_id
    ).first()

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )

    db.delete(question)
    db.commit()

    return {
        "message": "Question deleted successfully."
    }
