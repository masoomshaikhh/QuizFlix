from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    total_score: int
    quizzes_played: int
    accuracy: float

