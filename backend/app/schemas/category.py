
from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    category_name: str = Field(
        min_length=2,
        max_length=100
    )
    description: str | None = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: int
    category_name: str
    description: str | None = None


class CategoryUpdate(BaseModel):
    category_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    description: str | None = None

