
from backend.app.routers import users
from fastapi import FastAPI
from backend.app.routers import auth
from backend.app.routers import categories
from backend.app.routers import questions
from backend.app.routers import answer_options
from backend.app.routers import quizzes
from backend.app.routers import leaderboard
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import external_api

app = FastAPI(
    title="QuizFlix API",
    description="Backend API for the QuizFlix Movie and Music Trivia Platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(questions.router)
app.include_router(answer_options.router)
app.include_router(quizzes.router)
app.include_router(leaderboard.router)
app.include_router(external_api.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to QuizFlix API!",
        "status": "Running successfully"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
