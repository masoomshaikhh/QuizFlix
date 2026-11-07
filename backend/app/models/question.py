
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Question(Base):
    __tablename__ = "questions"

    question_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.category_id"),
        nullable=False
    )

    question_text = Column(
        Text,
        nullable=False
    )

    difficulty = Column(
        String(20),
        nullable=False
    )

    explanation = Column(
        Text,
        nullable=True
    )

    category = relationship("Category")
    options = relationship(
        "AnswerOption",
        back_populates="question",
        cascade="all, delete-orphan"
    )
