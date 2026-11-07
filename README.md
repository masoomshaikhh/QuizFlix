
# QuizFlix – Movie & Music Trivia Gaming Platform

QuizFlix is an interactive trivia gaming platform where users can test their knowledge of movies, music, web series and celebrities through multiple-choice quizzes.

The application provides user authentication, difficulty-based quizzes, score calculation, answer reviews, quiz history and a leaderboard.

## Features

- User registration and login.
- Secure password hashing and JWT authentication.
- Multiple entertainment categories:
  - Movies
  - Music
  - Web Series
  - Celebrities
- Easy, Medium and Hard difficulty levels.
- Randomized quiz question selection.
- Multiple-choice questions with four options.
- Server-side answer validation.
- Automatic score and accuracy calculation.
- Detailed answer review with explanations.
- Personal quiz history.
- Leaderboard with player rankings.
- Admin-controlled category and question management.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Database | MySQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Password Security | Passlib, bcrypt |
| API Testing | Pytest, FastAPI TestClient |
| Data Handling | Pandas, NumPy |
| Visualization | Matplotlib |
| Version Control | Git and GitHub |

## Project Structure

```text
QuizFlix/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_quizzes.py
│   │   ├── test_scoring.py
│   │   └── test_tdd_scoring.py
│   │
│   ├── requirements.txt
│   ├── create_tables.py
│   ├── seed_questions.py
│   └── seed_questions_batch2.py
│
├── frontend/
│   ├── index.html
│   ├── register.html
│   ├── dashboard.html
│   ├── quiz.html
│   ├── result.html
│   ├── style.css
│   └── JavaScript files
│
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/masoomshaikhh/QuizFlix.git
cd QuizFlix
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure MySQL Database

Create a MySQL database named:

```sql
CREATE DATABASE quizflix_db;
```

Configure the database connection and SECRET_KEY in the root `.env` file according to `backend/app/config.py`.

Never upload your actual `.env` file or database credentials to GitHub.

### 5. Create Database Tables

From the project root, run:

```bash
python -m backend.create_tables
```

### 6. Populate Quiz Questions

Run:

```bash
python -m backend.seed_questions
python -m backend.seed_questions_batch2
```

## Running the Application

### Start the Backend

From the project root:

```bash
uvicorn backend.app.main:app --reload
```

Backend URL:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### Start the Frontend

Open another terminal:

```bash
cd frontend
python -m http.server 5500
```

Open the application:

http://127.0.0.1:5500/index.html

## Main API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register` | Register a user |
| POST | `/api/auth/login` | Authenticate a user |
| GET | `/api/users/me` | Retrieve current user |
| POST | `/api/quizzes/start` | Start a quiz |
| POST | `/api/quizzes/{attempt_id}/submit` | Submit quiz answers |
| GET | `/api/quizzes/history` | Retrieve quiz history |
| GET | `/api/leaderboard/` | Retrieve leaderboard |

Additional category, question and answer-option endpoints are available in the API documentation.

## Testing

QuizFlix uses Pytest for automated testing.

Run the complete test suite:

```bash
python -m pytest -v
```

The current test suite covers:

- User registration and authentication.
- Duplicate account validation.
- Quiz creation and submission.
- Answer validation.
- Score calculation.
- Quiz history.
- Test-Driven Development of accuracy calculation.

**Latest verified test result:** 31 tests passed.

## Version Control

The project uses Git and GitHub for version control.

GitHub Repository:

https://github.com/masoomshaikhh/QuizFlix

Development is organized using Git branches and commits.

## Project Objective

The main objective of QuizFlix is to provide an engaging entertainment trivia experience while demonstrating software engineering principles, including modular development, database management, API development, authentication, automated testing and version control.

## Author

**Masoom Shaikh**

QuizFlix – Software Engineering Assignment
