
from backend.app.database import Base, engine
from backend.app import models

print("Creating QuizFlix database tables...")

Base.metadata.create_all(bind=engine)

print("All QuizFlix tables created successfully!")
