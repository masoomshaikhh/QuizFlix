
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.quiz import QuizAttempt
from backend.app.schemas.leaderboard import LeaderboardEntry

router = APIRouter(
    prefix="/api/leaderboard",
    tags=["Leaderboard"]
)


@router.get("/", response_model=list[LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):

    results = db.query(
        User.username,
        func.sum(QuizAttempt.score).label("total_score"),
        func.count(QuizAttempt.attempt_id).label("quizzes_played"),
        func.sum(QuizAttempt.correct_answers).label("total_correct"),
        func.sum(QuizAttempt.total_questions).label("total_questions")
    ).join(
        QuizAttempt,
        User.user_id == QuizAttempt.user_id
    ).filter(
        QuizAttempt.status == "completed"
    ).group_by(
        User.user_id,
        User.username
    ).order_by(
        func.sum(QuizAttempt.score).desc(),
        func.sum(QuizAttempt.correct_answers).desc()
    ).all()

    leaderboard = []

    for position, result in enumerate(results, start=1):

        total_correct = result.total_correct or 0
        total_questions = result.total_questions or 0

        accuracy = (
            round((total_correct / total_questions) * 100, 2)
            if total_questions > 0 else 0.0
        )

        leaderboard.append({
            "rank": position,
            "username": result.username,
            "total_score": result.total_score or 0,
            "quizzes_played": result.quizzes_played,
            "accuracy": accuracy
        })

    return leaderboard

