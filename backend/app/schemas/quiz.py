
from pydantic import BaseModel, Field
from datetime import datetime


# ==========================================
# START QUIZ
# ==========================================

class QuizStartRequest(BaseModel):
    category_id: int
    difficulty: str = Field(pattern="^(Easy|Medium|Hard)$")
    total_questions: int = Field(default=5, ge=1, le=20)


class QuizOptionResponse(BaseModel):
    option_id: int
    option_text: str


class QuizQuestionResponse(BaseModel):
    question_id: int
    question_text: str
    options: list[QuizOptionResponse]


class QuizStartResponse(BaseModel):
    attempt_id: int
    category_id: int
    difficulty: str
    total_questions: int
    questions: list[QuizQuestionResponse]


# ==========================================
# SUBMIT QUIZ
# ==========================================

class QuizAnswerSubmission(BaseModel):
    question_id: int
    selected_option_id: int


class QuizSubmitRequest(BaseModel):
    answers: list[QuizAnswerSubmission]


# ==========================================
# ANSWER REVIEW
# ==========================================

class QuizAnswerReview(BaseModel):
    question_id: int
    question_text: str

    selected_option_id: int
    selected_option_text: str

    correct_option_id: int
    correct_option_text: str

    is_correct: bool
    explanation: str | None = None


# ==========================================
# QUIZ RESULT
# ==========================================

class QuizResultResponse(BaseModel):
    attempt_id: int
    total_questions: int
    correct_answers: int
    score: int
    accuracy: float
    status: str

    review: list[QuizAnswerReview] = Field(default_factory=list)


# ==========================================
# QUIZ HISTORY
# ==========================================

class QuizHistoryResponse(BaseModel):
    attempt_id: int
    category_id: int
    difficulty: str
    total_questions: int
    correct_answers: int
    score: int
    status: str
    started_at: datetime
    completed_at: datetime | None
