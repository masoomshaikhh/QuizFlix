
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone

from backend.app.database import get_db

from backend.app.models.quiz import (
    AnswerOption,
    UserAnswer,
    QuizAttempt,
    QuizAttemptQuestion
)
from backend.app.models.question import Question
from backend.app.models.category import Category
from backend.app.models.user import User

from backend.app.schemas.quiz import (
    QuizStartRequest,
    QuizStartResponse,
    QuizSubmitRequest,
    QuizResultResponse,
    QuizHistoryResponse
)

from backend.app.services.dependencies import get_current_user
from backend.app.services.scoring import calculate_quiz_result


router = APIRouter(
    prefix="/api/quizzes",
    tags=["Quizzes"]
)


# ==========================================
# START A NEW QUIZ
# ==========================================

@router.post(
    "/start",
    response_model=QuizStartResponse,
    status_code=status.HTTP_201_CREATED
)
def start_quiz(
    request: QuizStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.category_id == request.category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found."
        )

    questions = db.query(Question).filter(
        Question.category_id == request.category_id,
        Question.difficulty == request.difficulty
    ).order_by(
        func.rand()
    ).limit(
        request.total_questions
    ).all()

    if len(questions) < request.total_questions:
        raise HTTPException(
            status_code=400,
            detail="Not enough questions available for this quiz."
        )

    attempt = QuizAttempt(
        user_id=current_user.user_id,
        category_id=request.category_id,
        difficulty=request.difficulty,
        total_questions=request.total_questions,
        correct_answers=0,
        score=0,
        status="in_progress"
    )

    try:
        db.add(attempt)
        db.flush()

        # Save the exact questions assigned to this attempt.
        assigned_questions = [
            QuizAttemptQuestion(
                attempt_id=attempt.attempt_id,
                question_id=question.question_id
            )
            for question in questions
        ]

        db.add_all(assigned_questions)
        db.commit()
        db.refresh(attempt)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not start the quiz."
        )

    quiz_questions = []

    for question in questions:
        quiz_questions.append({
            "question_id": question.question_id,
            "question_text": question.question_text,
            "options": [
                {
                    "option_id": option.option_id,
                    "option_text": option.option_text
                }
                for option in question.options
            ]
        })

    return {
        "attempt_id": attempt.attempt_id,
        "category_id": attempt.category_id,
        "difficulty": attempt.difficulty,
        "total_questions": attempt.total_questions,
        "questions": quiz_questions
    }


# ==========================================
# SUBMIT QUIZ ANSWERS AND GENERATE REVIEW
# ==========================================

@router.post(
    "/{attempt_id}/submit",
    response_model=QuizResultResponse
)
def submit_quiz(
    attempt_id: int,
    request: QuizSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.attempt_id == attempt_id,
        QuizAttempt.user_id == current_user.user_id
    ).first()

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Quiz attempt not found."
        )

    if attempt.status != "in_progress":
        raise HTTPException(
            status_code=400,
            detail="This quiz has already been submitted."
        )

    if len(request.answers) != attempt.total_questions:
        raise HTTPException(
            status_code=400,
            detail="Please submit an answer for every question."
        )

    question_ids = [
        answer.question_id for answer in request.answers
    ]

    if len(set(question_ids)) != len(question_ids):
        raise HTTPException(
            status_code=400,
            detail="Duplicate question answers are not allowed."
        )

    # Retrieve questions assigned to this quiz attempt.
    assigned_question_rows = db.query(
        QuizAttemptQuestion.question_id
    ).filter(
        QuizAttemptQuestion.attempt_id == attempt.attempt_id
    ).all()

    assigned_question_ids = {
        row[0] for row in assigned_question_rows
    }

    if set(question_ids) != assigned_question_ids:
        raise HTTPException(
            status_code=400,
            detail="Submitted questions do not match this quiz attempt."
        )

    correct_count = 0
    user_answers = []
    answer_reviews = []

    # Validate each answer and prepare its review.
    for answer in request.answers:

        question = db.query(Question).filter(
            Question.question_id == answer.question_id,
            Question.category_id == attempt.category_id,
            Question.difficulty == attempt.difficulty
        ).first()

        if question is None:
            raise HTTPException(
                status_code=400,
                detail="Invalid question submitted."
            )

        # Get the option selected by the player.
        selected_option = db.query(AnswerOption).filter(
            AnswerOption.option_id == answer.selected_option_id,
            AnswerOption.question_id == answer.question_id
        ).first()

        if selected_option is None:
            raise HTTPException(
                status_code=400,
                detail="Invalid answer option submitted."
            )

        # Find the actual correct option.
        correct_option = db.query(AnswerOption).filter(
            AnswerOption.question_id == answer.question_id,
            AnswerOption.is_correct == True
        ).first()

        if correct_option is None:
            raise HTTPException(
                status_code=500,
                detail="Correct answer is not configured for this question."
            )

        is_correct = bool(selected_option.is_correct)

        if is_correct:
            correct_count += 1

        # Save the player's answer in the database.
        user_answers.append(
            UserAnswer(
                attempt_id=attempt.attempt_id,
                question_id=answer.question_id,
                selected_option_id=answer.selected_option_id,
                is_correct=is_correct
            )
        )

        # Prepare answer review for the results page.
        answer_reviews.append({
            "question_id": question.question_id,
            "question_text": question.question_text,
            "selected_option_id": selected_option.option_id,
            "selected_option_text": selected_option.option_text,
            "correct_option_id": correct_option.option_id,
            "correct_option_text": correct_option.option_text,
            "is_correct": is_correct,
            "explanation": question.explanation
        })

    # Calculate score and accuracy using the tested scoring service.
    result = calculate_quiz_result(
        correct_count,
        attempt.total_questions
    )

    score = result["score"]
    accuracy = result["accuracy"]

    # Save completed quiz and answers.
    try:
        db.add_all(user_answers)

        attempt.correct_answers = correct_count
        attempt.score = score
        attempt.status = "completed"
        attempt.completed_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(attempt)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save quiz results."
        )

    # Return result together with answer review.
    return {
        "attempt_id": attempt.attempt_id,
        "total_questions": attempt.total_questions,
        "correct_answers": correct_count,
        "score": score,
        "accuracy": accuracy,
        "status": attempt.status,
        "review": answer_reviews
    }


# ==========================================
# GET QUIZ HISTORY
# ==========================================

@router.get(
    "/history",
    response_model=list[QuizHistoryResponse]
)
def get_quiz_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.user_id
    ).order_by(
        QuizAttempt.started_at.desc()
    ).all()

    return attempts
