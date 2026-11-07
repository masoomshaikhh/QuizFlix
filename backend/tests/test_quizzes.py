
import random
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql.sqltypes import String, Integer, Boolean, DateTime

from backend.app.main import app
from backend.app.database import Base, get_db
from backend.app.models.user import User
from backend.app.models.category import Category
from backend.app.models.question import Question
from backend.app.models.quiz import (
    AnswerOption,
    QuizAttempt,
    UserAnswer,
    QuizAttemptQuestion
)
from backend.app.services.dependencies import get_current_user


# ==========================================
# HELPER: CREATE MODEL RECORDS
# ==========================================

def create_record(db, model, **provided_values):
    """
    Creates a model record and supplies safe values
    for any other required columns.
    """
    values = dict(provided_values)

    for column in model.__table__.columns:

        if column.name in values:
            continue

        if column.primary_key and column.autoincrement:
            continue

        if column.nullable:
            continue

        if column.default is not None:
            continue

        if column.server_default is not None:
            continue

        name = column.name.lower()

        if isinstance(column.type, String):

            if "email" in name:
                values[column.name] = "tester@example.com"

            elif "username" in name:
                values[column.name] = "quiz_tester"

            elif "password" in name:
                values[column.name] = "test_password_hash"

            elif "role" in name:
                values[column.name] = "user"

            elif "difficulty" in name:
                values[column.name] = "Easy"

            elif "question_text" in name:
                values[column.name] = "Sample quiz question?"

            elif "explanation" in name:
                values[column.name] = "This is a test explanation."

            elif "category" in name or name == "name":
                values[column.name] = "Movies"

            else:
                values[column.name] = "Test data"

        elif isinstance(column.type, Boolean):
            values[column.name] = False

        elif isinstance(column.type, Integer):
            values[column.name] = 1

        elif isinstance(column.type, DateTime):
            values[column.name] = datetime.now(timezone.utc)

        else:
            values[column.name] = "Test data"

    record = model(**values)
    db.add(record)
    db.flush()

    return record


# ==========================================
# TEMPORARY SQLITE DATABASE
# ==========================================

@pytest.fixture
def db_session():

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    # SQLite does not provide MySQL's RAND() function.
    # Register a compatible function for the quiz router.
    def register_random_function(connection, record):
        connection.create_function(
            "rand",
            0,
            lambda: random.random()
        )

    event.listen(engine, "connect", register_random_function)

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    db = TestingSessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


# ==========================================
# TEST DATA
# ==========================================

@pytest.fixture
def quiz_data(db_session):

    user = create_record(
        db_session,
        User,
        username="quiz_tester",
        email="quiztester@example.com",
        password_hash="test_password_hash",
        role="user"
    )

    category = create_record(
        db_session,
        Category
    )

    questions = []
    correct_option_ids = {}
    option_ids = {}

    for number in range(1, 3):

        question = create_record(
            db_session,
            Question,
            category_id=category.category_id,
            question_text=f"Test question number {number}?",
            difficulty="Easy",
            explanation=f"Explanation for question {number}."
        )

        questions.append(question)

        option_ids[question.question_id] = []

        for option_number in range(1, 5):

            option = AnswerOption(
                question_id=question.question_id,
                option_text=f"Option {option_number}",
                is_correct=(option_number == 1)
            )

            db_session.add(option)
            db_session.flush()

            option_ids[question.question_id].append(
                option.option_id
            )

            if option.is_correct:
                correct_option_ids[question.question_id] = (
                    option.option_id
                )

    db_session.commit()

    return {
        "user": user,
        "category": category,
        "questions": questions,
        "correct_option_ids": correct_option_ids,
        "option_ids": option_ids
    }


# ==========================================
# FASTAPI TEST CLIENT
# ==========================================

@pytest.fixture
def client(db_session, quiz_data):

    def override_get_db():
        yield db_session

    def override_current_user():
        return quiz_data["user"]

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ==========================================
# HELPER: START QUIZ
# ==========================================

def start_test_quiz(client, category_id, total_questions=2):

    return client.post(
        "/api/quizzes/start",
        json={
            "category_id": category_id,
            "difficulty": "Easy",
            "total_questions": total_questions
        }
    )


# ==========================================
# HELPER: BUILD CORRECT ANSWERS
# ==========================================

def build_correct_answers(question_ids, quiz_data):

    answers = []

    for question_id in question_ids:

        answers.append({
            "question_id": question_id,
            "selected_option_id": (
                quiz_data["correct_option_ids"][question_id]
            )
        })

    return {"answers": answers}


# ==========================================
# TEST 1: START QUIZ SUCCESSFULLY
# ==========================================

def test_start_quiz_success(client, quiz_data):

    response = start_test_quiz(
        client,
        quiz_data["category"].category_id
    )

    assert response.status_code == 201

    data = response.json()

    assert data["attempt_id"] is not None
    assert data["category_id"] == quiz_data["category"].category_id
    assert data["difficulty"] == "Easy"
    assert data["total_questions"] == 2
    assert len(data["questions"]) == 2

    # Correct answers must not be revealed at quiz start.
    for question in data["questions"]:
        assert len(question["options"]) == 4

        for option in question["options"]:
            assert "is_correct" not in option


# ==========================================
# TEST 2: INVALID CATEGORY
# ==========================================

def test_start_quiz_invalid_category(client):

    response = start_test_quiz(
        client,
        category_id=99999
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found."


# ==========================================
# TEST 3: NOT ENOUGH QUESTIONS
# ==========================================

def test_start_quiz_not_enough_questions(client, quiz_data):

    response = start_test_quiz(
        client,
        quiz_data["category"].category_id,
        total_questions=3
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Not enough questions available for this quiz."
    )


# ==========================================
# TEST 4: SUCCESSFUL QUIZ SUBMISSION
# ==========================================

def test_submit_quiz_success(client, quiz_data):

    start_response = start_test_quiz(
        client,
        quiz_data["category"].category_id
    )

    attempt_id = start_response.json()["attempt_id"]

    question_ids = [
        question["question_id"]
        for question in start_response.json()["questions"]
    ]

    payload = build_correct_answers(
        question_ids,
        quiz_data
    )

    response = client.post(
        f"/api/quizzes/{attempt_id}/submit",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["attempt_id"] == attempt_id
    assert data["total_questions"] == 2
    assert data["correct_answers"] == 2
    assert data["score"] == 20
    assert data["accuracy"] == 100.0
    assert data["status"] == "completed"
    assert len(data["review"]) == 2

    for review in data["review"]:
        assert review["is_correct"] is True
        assert review["selected_option_id"] == (
            review["correct_option_id"]
        )


# ==========================================
# TEST 5: MISSING ANSWER
# ==========================================

def test_submit_quiz_missing_answer(client, quiz_data):

    start_response = start_test_quiz(
        client,
        quiz_data["category"].category_id
    )

    attempt_id = start_response.json()["attempt_id"]

    question_id = start_response.json()["questions"][0]["question_id"]

    payload = {
        "answers": [
            {
                "question_id": question_id,
                "selected_option_id": (
                    quiz_data["correct_option_ids"][question_id]
                )
            }
        ]
    }

    response = client.post(
        f"/api/quizzes/{attempt_id}/submit",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Please submit an answer for every question."
    )


# ==========================================
# TEST 6: DUPLICATE QUESTION SUBMISSION
# ==========================================

def test_submit_quiz_duplicate_questions(client, quiz_data):

    start_response = start_test_quiz(
        client,
        quiz_data["category"].category_id
    )

    attempt_id = start_response.json()["attempt_id"]

    question_id = start_response.json()["questions"][0]["question_id"]

    selected_option_id = (
        quiz_data["correct_option_ids"][question_id]
    )

    payload = {
        "answers": [
            {
                "question_id": question_id,
                "selected_option_id": selected_option_id
            },
            {
                "question_id": question_id,
                "selected_option_id": selected_option_id
            }
        ]
    }

    response = client.post(
        f"/api/quizzes/{attempt_id}/submit",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Duplicate question answers are not allowed."
    )


# ==========================================
# TEST 7: QUESTION NOT ASSIGNED TO ATTEMPT
# ==========================================

def test_submit_quiz_unassigned_question(client, quiz_data, db_session):

    start_response = start_test_quiz(
        client,
        quiz_data["category"].category_id
    )

    attempt_id = start_response.json()["attempt_id"]

    assigned_ids = [
        question["question_id"]
        for question in start_response.json()["questions"]
    ]

    # Create another valid question after the quiz has started.
    extra_question = create_record(
        db_session,
        Question,
        category_id=quiz_data["category"].category_id,
        question_text="Question not assigned to this quiz?",
        difficulty="Easy",
        explanation="Extra test question."
    )

    db_session.commit()

    payload = {
        "answers": [
            {
                "question_id": assigned_ids[0],
                "selected_option_id": (
                    quiz_data["correct_option_ids"][assigned_ids[0]]
                )
            },
            {
                "question_id": extra_question.question_id,
                "selected_option_id": 99999
            }
        ]
    }

    response = client.post(
        f"/api/quizzes/{attempt_id}/submit",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Submitted questions do not match this quiz attempt."
    )


# ==========================================
# TEST 8: INVALID OPTION FOR QUESTION
# ==========================================

def test_submit_quiz_invalid_option(client, quiz_data):

    start_response = start_test_quiz(
        client,
        quiz_data["category"].category_id
    )

    attempt_id = start_response.json()["attempt_id"]

    question_ids = [
        question["question_id"]
        for question in start_response.json()["questions"]
    ]

    first_question = question_ids[0]
    second_question = question_ids[1]

    # Use an option that belongs to the second question
    # for the first question.
    wrong_option_id = quiz_data["option_ids"][second_question][0]

    payload = {
        "answers": [
            {
                "question_id": first_question,
                "selected_option_id": wrong_option_id
            },
            {
                "question_id": second_question,
                "selected_option_id": (
                    quiz_data["correct_option_ids"][second_question]
                )
            }
        ]
    }

    response = client.post(
        f"/api/quizzes/{attempt_id}/submit",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Invalid answer option submitted."
    )


# ==========================================
# TEST 9: SUBMIT ALREADY COMPLETED QUIZ
# ==========================================

def test_submit_quiz_twice(client, quiz_data):

    start_response = start_test_quiz(
        client,
        quiz_data["category"].category_id
    )

    attempt_id = start_response.json()["attempt_id"]

    question_ids = [
        question["question_id"]
        for question in start_response.json()["questions"]
    ]

    payload = build_correct_answers(
        question_ids,
        quiz_data
    )

    first_response = client.post(
        f"/api/quizzes/{attempt_id}/submit",
        json=payload
    )

    assert first_response.status_code == 200

    second_response = client.post(
        f"/api/quizzes/{attempt_id}/submit",
        json=payload
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == (
        "This quiz has already been submitted."
    )


# ==========================================
# TEST 10: GET QUIZ HISTORY
# ==========================================

def test_get_quiz_history(client, quiz_data):

    start_response = start_test_quiz(
        client,
        quiz_data["category"].category_id
    )

    attempt_id = start_response.json()["attempt_id"]

    question_ids = [
        question["question_id"]
        for question in start_response.json()["questions"]
    ]

    payload = build_correct_answers(
        question_ids,
        quiz_data
    )

    submit_response = client.post(
        f"/api/quizzes/{attempt_id}/submit",
        json=payload
    )

    assert submit_response.status_code == 200

    history_response = client.get(
        "/api/quizzes/history"
    )

    assert history_response.status_code == 200

    history = history_response.json()

    assert len(history) == 1
    assert history[0]["attempt_id"] == attempt_id
    assert history[0]["total_questions"] == 2
    assert history[0]["correct_answers"] == 2
    assert history[0]["score"] == 20
    assert history[0]["status"] == "completed"
