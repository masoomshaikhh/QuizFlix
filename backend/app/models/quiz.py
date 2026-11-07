
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class AnswerOption(Base):
    __tablename__ = "answer_options"

    option_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.question_id"),
        nullable=False
    )

    option_text = Column(
        String(500),
        nullable=False
    )

    is_correct = Column(
        Boolean,
        default=False,
        nullable=False
    )

    question = relationship(
        "Question",
        back_populates="options"
    )


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    attempt_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.category_id"),
        nullable=False
    )

    difficulty = Column(
        String(20),
        nullable=False
    )

    total_questions = Column(
        Integer,
        nullable=False
    )

    correct_answers = Column(
        Integer,
        default=0,
        nullable=False
    )

    score = Column(
        Integer,
        default=0,
        nullable=False
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    status = Column(
        String(20),
        default="in_progress",
        nullable=False
    )


class UserAnswer(Base):
    __tablename__ = "user_answers"

    answer_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    attempt_id = Column(
        Integer,
        ForeignKey("quiz_attempts.attempt_id"),
        nullable=False
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.question_id"),
        nullable=False
    )

    selected_option_id = Column(
        Integer,
        ForeignKey("answer_options.option_id"),
        nullable=True
    )

    is_correct = Column(
        Boolean,
        default=False,
        nullable=False
    )


class QuizAttemptQuestion(Base):
    __tablename__ = "quiz_attempt_questions"

    attempt_id = Column(
        Integer,
        ForeignKey("quiz_attempts.attempt_id"),
        primary_key=True
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.question_id"),
        primary_key=True
    )
