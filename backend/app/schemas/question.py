
from pydantic import BaseModel, ConfigDict, Field


class QuestionCreate(BaseModel):
    category_id: int
    question_text: str = Field(min_length=5)
    difficulty: str = Field(pattern="^(Easy|Medium|Hard)$")
    explanation: str | None = None


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question_id: int
    category_id: int
    question_text: str
    difficulty: str
    explanation: str | None = None

class QuestionUpdate(BaseModel):
    category_id: int | None = None
    question_text: str | None = Field(default=None, min_length=5)
    difficulty: str | None = Field(
        default=None,
        pattern="^(Easy|Medium|Hard)$"
    )
    explanation: str | None = None