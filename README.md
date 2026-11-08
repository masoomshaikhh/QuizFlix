# QuizFlix – Movie & Music Trivia Gaming Platform

QuizFlix is an interactive web-based trivia gaming platform where users can test their knowledge of movies, music, web series and celebrities through multiple-choice quizzes.

The application provides user authentication, difficulty-based quizzes, randomized question selection, automatic scoring, answer reviews, quiz history and leaderboard functionality.

It also integrates the Apple iTunes Search API to retrieve external entertainment metadata.

## Features

- User registration and login.
- Secure password hashing and JWT authentication.
- Four entertainment categories:
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
- Personal quiz history with refresh functionality.
- Dashboard statistics.
- Leaderboard with player rankings.
- Admin-controlled category and question management.
- External movie, music and television searches using the Apple iTunes Search API.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Database | MySQL |
| ORM | SQLAlchemy |
| Database Driver | PyMySQL |
| Authentication | JWT |
| Password Security | Passlib, bcrypt |
| External API Requests | Python Requests |
| External API | Apple iTunes Search API |
| Automated Testing | Pytest, FastAPI TestClient |
| Data Handling | Pandas, NumPy |
| Visualization | Matplotlib |
| Machine Learning | Scikit-learn |
| Version Control | Git and GitHub |
| Continuous Integration | GitHub Actions |

## Project Structure

```text
QuizFlix/
│
├── backend/
│   │
│   ├── app/
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── category.py
│   │   │   ├── question.py
│   │   │   └── quiz.py
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── categories.py
│   │   │   ├── questions.py
│   │   │   ├── answer_options.py
│   │   │   ├── quizzes.py
│   │   │   ├── leaderboard.py
│   │   │   └── external_api.py
│   │   │
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_crud_methods.py
│   │   ├── test_external_api.py
│   │   ├── test_quizzes.py
│   │   ├── test_scoring.py
│   │   └── test_tdd_scoring.py
│   │
│   ├── analytics/
│   │   ├── analyze_quizflix.py
│   │   ├── data_science_model.py
│   │   ├── run_performance.py
│   │   ├── quizflix_analytics.csv
│   │   ├── quizflix_ml_training_data.csv
│   │   ├── performance_results.csv
│   │   ├── http_method_results.csv
│   │   └── Generated charts and cleaned datasets
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
│   ├── script.js
│   ├── register.js
│   ├── dashboard.js
│   ├── quiz.js
│   └── result.js
│
├── docs/
│   ├── SRS.md
│   ├── sdlc_v_model.md
│   ├── system_architecture.md
│   ├── database_design_and_erd.md
│   ├── functional_testing_report.md
│   ├── performance_testing_report.md
│   └── final_project_report.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── README.md
└── .env (local configuration; not committed)
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

Activate it on Windows PowerShell:

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

Configure the database connection and secret key in the root `.env` file according to `backend/app/config.py`.

The configuration uses the following environment variables:

```text
DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_NAME
SECRET_KEY
```

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

API Documentation:

http://127.0.0.1:8000/docs

### Start the Frontend

Open another terminal:

```powershell
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
| GET | `/api/external/search` | Search external entertainment content |

Additional category, question and answer-option endpoints are available in the FastAPI documentation.

## Testing

QuizFlix uses Pytest and FastAPI TestClient for automated testing.

Run the complete test suite:

```bash
python -m pytest -v
```

The automated test suite contains 44 tests covering:

- User registration and authentication.
- Duplicate account validation.
- Quiz creation and submission.
- Answer validation.
- Score and accuracy calculation.
- Quiz history retrieval.
- Test-Driven Development.
- External API integration and error handling.
- Category CRUD operations.

**Latest verified local test result: 44 passed, 0 failed.**

One non-fatal deprecation warning involving Starlette and HTTPX was reported.

## Functional and Performance Testing

The project includes functional and performance testing activities.

Functional testing covers user authentication, quiz participation, answer submission, scoring, quiz history, leaderboard operations and external API handling.

Browser-level testing was also performed using Google Chrome.

Performance testing includes sequential and concurrent API requests to evaluate:

- Response times.
- Throughput.
- Error rates.
- Response-time percentiles.

Detailed test cases and results are available in the `docs` folder.

## Data Analytics and Machine Learning

QuizFlix includes academic data analytics and machine-learning demonstrations.

**Data Analytics**

Pandas and NumPy are used for data processing, cleaning, aggregation and statistical analysis. Matplotlib is used to generate visualizations.

**Machine Learning**

A Scikit-learn Decision Tree Classifier is used to demonstrate classification of quiz difficulty using simulated quiz-performance data.

The analytics and machine-learning datasets are simulated and are not actual user activity records from the live application.

## External API Integration

QuizFlix integrates with the Apple iTunes Search API to retrieve external entertainment metadata.

Supported search types include:

- Movies.
- Music.
- Television shows.

The integration uses Python Requests, processes JSON responses and handles invalid requests, timeouts and connection errors.

## Continuous Integration

GitHub Actions is configured to install project dependencies and automatically execute the Pytest suite.

The workflow runs on:

- Pushes to the `main` branch.
- Pull requests targeting the `main` branch.

The project includes a verified CI demonstration involving an intentional test failure followed by a successful correction.

## Documentation

The `docs` folder contains the project's documentation:

| Document | Description |
|---|---|
| SRS.md | Software Requirements Specification |
| sdlc_v_model.md | V-Model SDLC documentation |
| system_architecture.md | System architecture |
| database_design_and_erd.md | Database design and ER diagram |
| functional_testing_report.md | Functional testing report |
| performance_testing_report.md | Performance testing report |
| final_project_report.md | Main software engineering project report |

## Version Control

The project uses Git and GitHub for version control.

GitHub Repository:

https://github.com/masoomshaikhh/QuizFlix

Development is managed using Git branches, commits and pull requests.

## Project Objective

The main objective of QuizFlix is to provide an engaging entertainment trivia experience while demonstrating software engineering principles, including modular development, database management, API development, authentication, automated testing, data analysis and version control.

## Author

**Masoom Shaikh**

QuizFlix – Software Engineering Assignment