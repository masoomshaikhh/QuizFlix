
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.question import Question
from backend.app.models.quiz import AnswerOption
from backend.app.schemas.answer_option import (
    AnswerOptionCreate,
    AnswerOptionResponse,
    AnswerOptionUpdate
)
from backend.app.services.dependencies import get_admin_user
from backend.app.models.user import User


router = APIRouter(
    prefix="/api/questions",
    tags=["Answer Options"]
)


@router.post(
    "/{question_id}/options",
    response_model=list[AnswerOptionResponse],
    status_code=status.HTTP_201_CREATED
)
def add_answer_options(
    question_id: int,
    options: list[AnswerOptionCreate],
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

    if len(options) != 4:
        raise HTTPException(
            status_code=400,
            detail="Exactly four answer options are required."
        )

    correct_count = sum(option.is_correct for option in options)

    if correct_count != 1:
        raise HTTPException(
            status_code=400,
            detail="Exactly one option must be correct."
        )

    existing_options = db.query(AnswerOption).filter(
        AnswerOption.question_id == question_id
    ).first()

    if existing_options:
        raise HTTPException(
            status_code=409,
            detail="Answer options already exist for this question."
        )

    new_options = [
        AnswerOption(
            question_id=question_id,
            option_text=option.option_text,
            is_correct=option.is_correct
        )
        for option in options
    ]

    db.add_all(new_options)
    db.commit()

    for option in new_options:
        db.refresh(option)

    return new_options


@router.get(
    "/{question_id}/options",
    response_model=list[AnswerOptionResponse]
)
def get_answer_options(
    question_id: int,
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(
        Question.question_id == question_id
    ).first()

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )

    return db.query(AnswerOption).filter(
        AnswerOption.question_id == question_id
    ).order_by(AnswerOption.option_id).all()


@router.put(
    "/{question_id}/options/{option_id}",
    response_model=AnswerOptionResponse
)
def update_answer_option(
    question_id: int,
    option_id: int,
    option_data: AnswerOptionUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    option = db.query(AnswerOption).filter(
        AnswerOption.option_id == option_id,
        AnswerOption.question_id == question_id
    ).first()

    if option is None:
        raise HTTPException(
            status_code=404,
            detail="Answer option not found."
        )

    update_data = option_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No update information provided."
        )

    if "is_correct" in update_data:
        if update_data["is_correct"] is True:
            db.query(AnswerOption).filter(
                AnswerOption.question_id == question_id
            ).update(
                {AnswerOption.is_correct: False},
                synchronize_session=False
            )

        elif update_data["is_correct"] is False:
            other_correct = db.query(AnswerOption).filter(
                AnswerOption.question_id == question_id,
                AnswerOption.option_id != option_id,
                AnswerOption.is_correct == True
            ).first()

            if other_correct is None:
                raise HTTPException(
                    status_code=400,
                    detail="A question must have exactly one correct option."
                )

    for key, value in update_data.items():
        setattr(option, key, value)

    db.commit()
    db.refresh(option)

    return option


@router.delete("/{question_id}/options/{option_id}")
def delete_answer_option(
    question_id: int,
    option_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    option = db.query(AnswerOption).filter(
        AnswerOption.option_id == option_id,
        AnswerOption.question_id == question_id
    ).first()

    if option is None:
        raise HTTPException(
            status_code=404,
            detail="Answer option not found."
        )

    total_options = db.query(AnswerOption).filter(
        AnswerOption.question_id == question_id
    ).count()

    if total_options <= 4:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete an option. Each question must have exactly four options."
        )

    db.delete(option)
    db.commit()

    return {
        "message": "Answer option deleted successfully."
    }
