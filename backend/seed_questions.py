
from backend.app.database import SessionLocal
from backend.app.models.category import Category
from backend.app.models.question import Question
from backend.app.models.quiz import AnswerOption


# ==========================================
# QUIZFLIX - INITIAL QUESTION BANK
# 12 Questions | 4 Categories | 3 Difficulty Levels
# ==========================================

questions_data = [

    # ======================================
    # 1. MOVIES
    # ======================================

    {
        "category": "Movies",
        "difficulty": "Easy",
        "question": "Which superhero is also known as the Friendly Neighborhood Spider-Man?",
        "options": [
            "Bruce Wayne",
            "Peter Parker",
            "Clark Kent",
            "Tony Stark"
        ],
        "correct": 1,
        "explanation": "Peter Parker is the identity of Spider-Man, the Marvel superhero."
    },

    {
        "category": "Movies",
        "difficulty": "Medium",
        "question": "Who directed the movie Avatar (2009)?",
        "options": [
            "Christopher Nolan",
            "Steven Spielberg",
            "James Cameron",
            "Ridley Scott"
        ],
        "correct": 2,
        "explanation": "James Cameron directed Avatar, released in 2009."
    },

    {
        "category": "Movies",
        "difficulty": "Hard",
        "question": "What is the name of the black hole in the movie Interstellar?",
        "options": [
            "Sagittarius A*",
            "Gargantua",
            "Cygnus X-1",
            "Ton 618"
        ],
        "correct": 1,
        "explanation": "Gargantua is the massive rotating black hole featured in Interstellar."
    },

    # ======================================
    # 2. WEB SERIES
    # ======================================

    {
        "category": "Web Series",
        "difficulty": "Easy",
        "question": "What is the name of the coffee shop frequently visited by the friends in Friends?",
        "options": [
            "Central Perk",
            "Monk's Cafe",
            "MacLaren's Pub",
            "Luke's Diner"
        ],
        "correct": 0,
        "explanation": "Central Perk is the famous coffee shop where the Friends characters regularly meet."
    },

    {
        "category": "Web Series",
        "difficulty": "Medium",
        "question": "What is the name of the fictional town where Stranger Things is primarily set?",
        "options": [
            "Riverdale",
            "Mystic Falls",
            "Hawkins",
            "Derry"
        ],
        "correct": 2,
        "explanation": "Stranger Things is primarily set in Hawkins, Indiana."
    },

    {
        "category": "Web Series",
        "difficulty": "Hard",
        "question": "In IT: Welcome to Derry, what is the name of the fictional town where the story takes place?",
        "options": [
            "Castle Rock",
            "Hawkins",
            "Derry",
            "Jericho"
        ],
        "correct": 2,
        "explanation": "Welcome to Derry is set in the fictional town of Derry, Maine."
    },

    # ======================================
    # 3. MUSIC
    # ======================================

    {
        "category": "Music",
        "difficulty": "Easy",
        "question": "Which electronic music duo released the hit song Closer featuring Halsey?",
        "options": [
            "Marshmello",
            "The Chainsmokers",
            "Daft Punk",
            "Disclosure"
        ],
        "correct": 1,
        "explanation": "The Chainsmokers released Closer featuring Halsey in 2016."
    },

    {
        "category": "Music",
        "difficulty": "Medium",
        "question": "Which song by One Direction was released as the lead single from their album Four?",
        "options": [
            "What Makes You Beautiful",
            "Story of My Life",
            "Steal My Girl",
            "Night Changes"
        ],
        "correct": 2,
        "explanation": "Steal My Girl was released as the lead single from One Direction's fourth studio album, Four."
    },

    {
        "category": "Music",
        "difficulty": "Hard",
        "question": "Which Indian composer won two Academy Awards for his work on Slumdog Millionaire?",
        "options": [
            "Pritam",
            "Amit Trivedi",
            "A. R. Rahman",
            "Vishal-Shekhar"
        ],
        "correct": 2,
        "explanation": "A. R. Rahman won two Academy Awards for Slumdog Millionaire."
    },

    # ======================================
    # 4. CELEBRITIES
    # ======================================

    {
        "category": "Celebrities",
        "difficulty": "Easy",
        "question": "Which actor portrays Tony Stark, also known as Iron Man, in the Marvel Cinematic Universe?",
        "options": [
            "Chris Evans",
            "Robert Downey Jr.",
            "Chris Hemsworth",
            "Mark Ruffalo"
        ],
        "correct": 1,
        "explanation": "Robert Downey Jr. portrays Tony Stark, also known as Iron Man."
    },

    {
        "category": "Celebrities",
        "difficulty": "Medium",
        "question": "Which singer released the album 1989?",
        "options": [
            "Ariana Grande",
            "Rihanna",
            "Taylor Swift",
            "Selena Gomez"
        ],
        "correct": 2,
        "explanation": "1989 is a studio album released by Taylor Swift in 2014."
    },

    {
        "category": "Celebrities",
        "difficulty": "Hard",
        "question": "Which legendary Indian singer was awarded the Bharat Ratna in 2001?",
        "options": [
            "Asha Bhosle",
            "Shreya Ghoshal",
            "Lata Mangeshkar",
            "Sunidhi Chauhan"
        ],
        "correct": 2,
        "explanation": "Lata Mangeshkar received India's highest civilian award, the Bharat Ratna, in 2001."
    }
]


# ==========================================
# INSERT QUESTIONS INTO MYSQL DATABASE
# ==========================================

def seed_questions():

    db = SessionLocal()

    inserted_count = 0
    skipped_count = 0

    try:

        for item in questions_data:

            # Find category using its name
            category = db.query(Category).filter(
                Category.category_name == item["category"]
            ).first()

            if not category:
                raise ValueError(
                    f"Category not found: {item['category']}"
                )

            # Prevent duplicate questions
            existing_question = db.query(Question).filter(
                Question.category_id == category.category_id,
                Question.question_text == item["question"]
            ).first()

            if existing_question:
                print(
                    f"Skipped duplicate: {item['question']}"
                )
                skipped_count += 1
                continue

            # Create the question
            new_question = Question(
                category_id=category.category_id,
                question_text=item["question"],
                difficulty=item["difficulty"],
                explanation=item["explanation"]
            )

            db.add(new_question)
            db.flush()

            # Create four answer options
            for index, option_text in enumerate(item["options"]):

                new_option = AnswerOption(
                    question_id=new_question.question_id,
                    option_text=option_text,
                    is_correct=(index == item["correct"])
                )

                db.add(new_option)

            inserted_count += 1

            print(
                f"Added: {item['category']} | "
                f"{item['difficulty']} | "
                f"{item['question']}"
            )

        # Save all changes
        db.commit()

        print("\n================================")
        print("QUIZFLIX QUESTION BANK COMPLETE")
        print("================================")
        print(f"Questions inserted: {inserted_count}")
        print(f"Questions skipped: {skipped_count}")
        print(f"Total questions in batch: {len(questions_data)}")
        print("Database changes committed successfully!")

    except Exception as error:

        db.rollback()

        print("\nError while inserting questions:")
        print(error)

        raise

    finally:

        db.close()


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    seed_questions()
