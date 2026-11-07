
from pydantic import BaseModel, ConfigDict, Field


class AnswerOptionCreate(BaseModel):
    option_text: str = Field(min_length=1, max_length=500)
    is_correct: bool = False


class AnswerOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    option_id: int
    question_id: int
    option_text: str


class AnswerOptionUpdate(BaseModel):
    option_text: str | None = Field(
        default=None,
        min_length=1,
        max_length=500
    )
    is_correct: bool | None = None
