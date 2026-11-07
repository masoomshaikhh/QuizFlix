
from backend.app.database import SessionLocal
from backend.app.models.category import Category
from backend.app.models.question import Question
from backend.app.models.quiz import AnswerOption


# ==================================================
# QUIZFLIX - QUESTION BANK BATCH 2
# 48 New Questions | 12 Per Category
# ==================================================

# Format:
# Category, Difficulty, Question, Options, Correct Index, Explanation

questions_data = [

    # ==================================================
    # 1. MOVIES
    # ==================================================

    (
        "Movies", "Easy",
        "What is the name of the wizarding school Harry Potter attends?",
        ["Beauxbatons", "Hogwarts", "Durmstrang", "Ilvermorny"],
        1,
        "Hogwarts School of Witchcraft and Wizardry is where Harry and his friends study."
    ),

    (
        "Movies", "Easy",
        "In Marvel movies, Thor is the God of which realm?",
        ["Midgard", "Wakanda", "Asgard", "Knowhere"],
        2,
        "Thor is the Asgardian God of Thunder."
    ),

    (
        "Movies", "Easy",
        "Which fictional planet or moon is home to the Na'vi in Avatar?",
        ["Krypton", "Pandora", "Tatooine", "Vulcan"],
        1,
        "Pandora is the fictional moon inhabited by the Na'vi in Avatar."
    ),

    (
        "Movies", "Easy",
        "Who plays Dominic Toretto in the Fast & Furious franchise?",
        ["Jason Statham", "Paul Walker", "Vin Diesel", "Dwayne Johnson"],
        2,
        "Vin Diesel portrays Dominic Toretto in the Fast & Furious films."
    ),

    (
        "Movies", "Medium",
        "Who directed The Dark Knight (2008)?",
        ["James Cameron", "Christopher Nolan", "Zack Snyder", "Tim Burton"],
        1,
        "Christopher Nolan directed The Dark Knight."
    ),

    (
        "Movies", "Medium",
        "Who directed the movie Titanic (1997)?",
        ["Steven Spielberg", "James Cameron", "Ridley Scott", "Peter Jackson"],
        1,
        "James Cameron directed the 1997 film Titanic."
    ),

    (
        "Movies", "Medium",
        "What is the name of the island where Jurassic Park is located?",
        ["Isla Sorna", "Isla Nublar", "Skull Island", "Isla Muerta"],
        1,
        "Isla Nublar is the fictional island where the original Jurassic Park is established."
    ),

    (
        "Movies", "Medium",
        "In The Hunger Games, which district is Katniss Everdeen from?",
        ["District 1", "District 4", "District 12", "District 13"],
        2,
        "Katniss Everdeen comes from District 12."
    ),

    (
        "Movies", "Medium",
        "What is the surname of Don Vito, the central character in The Godfather?",
        ["Soprano", "Corleone", "Barzini", "Tattaglia"],
        1,
        "Vito Corleone is the central patriarch in The Godfather."
    ),

    (
        "Movies", "Hard",
        "What is the name of the wizarding prison guarded by Dementors in Harry Potter?",
        ["Hogwarts", "Azkaban", "Gringotts", "Nurmengard"],
        1,
        "Azkaban is the wizarding prison guarded by Dementors."
    ),

    (
        "Movies", "Hard",
        "What is the fictional country ruled by T'Challa in Black Panther?",
        ["Genosha", "Latveria", "Wakanda", "Sokovia"],
        2,
        "Wakanda is the fictional African nation ruled by T'Challa."
    ),

    (
        "Movies", "Hard",
        "What organization does Ethan Hunt work for in Mission: Impossible?",
        [
            "S.H.I.E.L.D.",
            "Impossible Mission Force",
            "Kingsman",
            "CIA Special Activities Center"
        ],
        1,
        "Ethan Hunt works for the Impossible Mission Force, commonly called the IMF."
    ),

    # ==================================================
    # 2. WEB SERIES
    # ==================================================

    (
        "Web Series", "Easy",
        "What is the name of the main female character in The Vampire Diaries?",
        ["Caroline Forbes", "Bonnie Bennett", "Elena Gilbert", "Rebekah Mikaelson"],
        2,
        "Elena Gilbert is the central female character in The Vampire Diaries."
    ),

    (
        "Web Series", "Easy",
        "What name does Walter White use in Breaking Bad?",
        ["Saul", "Heisenberg", "Gus", "Tuco"],
        1,
        "Walter White uses the alias Heisenberg in his criminal activities."
    ),

    (
        "Web Series", "Easy",
        "What is the name of Sheldon Cooper's roommate in The Big Bang Theory?",
        ["Howard Wolowitz", "Raj Koothrappali", "Leonard Hofstadter", "Stuart Bloom"],
        2,
        "Leonard Hofstadter is Sheldon's roommate and close friend."
    ),

    (
        "Web Series", "Easy",
        "What is the name of Sherlock Holmes's famous London address in Sherlock?",
        ["10 Downing Street", "221B Baker Street", "12 Grimmauld Place", "4 Privet Drive"],
        1,
        "Sherlock Holmes lives at 221B Baker Street."
    ),

    (
        "Web Series", "Medium",
        "In Game of Thrones, which House has the motto 'Winter Is Coming'?",
        ["House Lannister", "House Targaryen", "House Stark", "House Baratheon"],
        2,
        "Winter Is Coming is the motto of House Stark."
    ),

    (
        "Web Series", "Medium",
        "What is the real name of the Professor in Money Heist?",
        ["Andrés de Fonollosa", "Sergio Marquina", "Aníbal Cortés", "Agustín Ramos"],
        1,
        "The Professor's real name is Sergio Marquina."
    ),

    (
        "Web Series", "Medium",
        "What is the name of the school Wednesday Addams attends in Wednesday?",
        ["Hawkins High", "Nevermore Academy", "Briarcliff Academy", "Salvatore School"],
        1,
        "Wednesday attends Nevermore Academy."
    ),

    (
        "Web Series", "Medium",
        "What is the name of the superhero group in The Boys?",
        ["The Guardians", "The Seven", "The Avengers", "The Defenders"],
        1,
        "The Seven is Vought International's famous superhero team."
    ),

    (
        "Web Series", "Hard",
        "What is the name of the town where the German series Dark takes place?",
        ["Winden", "Derry", "Hawkins", "Jericho"],
        0,
        "Dark takes place in the fictional German town of Winden."
    ),

    (
        "Web Series", "Hard",
        "What is the total prize money in the first season of Squid Game?",
        ["10 billion won", "25 billion won", "45.6 billion won", "100 billion won"],
        2,
        "The prize money in Squid Game is 45.6 billion South Korean won."
    ),

    (
        "Web Series", "Hard",
        "What is Belly's full first name in The Summer I Turned Pretty?",
        ["Isabel", "Isabella", "Elizabeth", "Annabelle"],
        0,
        "Belly is short for Isabel in The Summer I Turned Pretty."
    ),

    (
        "Web Series", "Hard",
        "Welcome to Derry is based on which novel by Stephen King?",
        ["The Shining", "Carrie", "IT", "Misery"],
        2,
        "Welcome to Derry expands the story and world of Stephen King's novel IT."
    ),

    # ==================================================
    # 3. MUSIC
    # ==================================================

    (
        "Music", "Easy",
        "What is the name of BTS's first English-language single?",
        ["Butter", "Dynamite", "Permission to Dance", "Boy With Luv"],
        1,
        "Dynamite was BTS's first song released entirely in English."
    ),

    (
        "Music", "Easy",
        "What is the official fandom name of SEVENTEEN?",
        ["ARMY", "BLINK", "CARAT", "STAY"],
        2,
        "SEVENTEEN fans are officially known as CARAT."
    ),

    (
        "Music", "Easy",
        "What is the official fandom name of BLACKPINK?",
        ["BLINK", "ONCE", "MOA", "MIDZY"],
        0,
        "BLACKPINK fans are officially known as BLINK."
    ),

    (
        "Music", "Easy",
        "What is the official fandom name of Stray Kids?",
        ["ENGENE", "STAY", "ATINY", "EXO-L"],
        1,
        "Stray Kids fans are known as STAY."
    ),

    (
        "Music", "Medium",
        "Through which television competition was One Direction formed?",
        ["The Voice", "American Idol", "The X Factor", "Britain's Got Talent"],
        2,
        "One Direction was formed during the 2010 season of The X Factor UK."
    ),

    (
        "Music", "Medium",
        "Which group collaborated with Coldplay on the song Something Just Like This?",
        ["Daft Punk", "The Chainsmokers", "Maroon 5", "Imagine Dragons"],
        1,
        "The Chainsmokers collaborated with Coldplay on Something Just Like This."
    ),

    (
        "Music", "Medium",
        "Which Taylor Swift album includes the songs Cardigan and August?",
        ["1989", "Lover", "Folklore", "Midnights"],
        2,
        "Cardigan and August are both songs from Taylor Swift's album Folklore."
    ),

    (
        "Music", "Medium",
        "Which Bollywood film features Arijit Singh's popular song Tum Hi Ho?",
        ["Yeh Jawaani Hai Deewani", "Aashiqui 2", "Barfi!", "Kabir Singh"],
        1,
        "Tum Hi Ho is a popular song from the film Aashiqui 2."
    ),

    (
        "Music", "Medium",
        "Which film features Shreya Ghoshal's song Bairi Piya?",
        ["Devdas", "Jodhaa Akbar", "Veer-Zaara", "Ram-Leela"],
        0,
        "Bairi Piya is a song from Sanjay Leela Bhansali's film Devdas."
    ),

    (
        "Music", "Hard",
        "Which song from Slumdog Millionaire won A. R. Rahman an Academy Award for Best Original Song?",
        ["Maa Tujhe Salaam", "Jai Ho", "Vande Mataram", "Chaiyya Chaiyya"],
        1,
        "Jai Ho won the Academy Award for Best Original Song."
    ),

    (
        "Music", "Hard",
        "Which Indian singer is widely known by the nickname 'King of Playback Singing' in Punjabi music?",
        ["Diljit Dosanjh", "Sonu Nigam", "Arijit Singh", "Kumar Sanu"],
        0,
        "Diljit Dosanjh is a prominent Punjabi singer and performer."
    ),

    (
        "Music", "Hard",
        "Which dance move is famously associated with Michael Jackson?",
        ["The Robot", "The Moonwalk", "The Charleston", "The Twist"],
        1,
        "Michael Jackson made the Moonwalk internationally famous through his performances."
    ),

    # ==================================================
    # 4. CELEBRITIES
    # ==================================================

    (
        "Celebrities", "Easy",
        "Which actor played Harry Potter in the film series?",
        ["Rupert Grint", "Daniel Radcliffe", "Tom Felton", "Matthew Lewis"],
        1,
        "Daniel Radcliffe portrayed Harry Potter in all eight main Harry Potter films."
    ),

    (
        "Celebrities", "Easy",
        "Which actress played Hermione Granger in the Harry Potter films?",
        ["Emma Stone", "Keira Knightley", "Emma Watson", "Anne Hathaway"],
        2,
        "Emma Watson portrayed Hermione Granger."
    ),

    (
        "Celebrities", "Easy",
        "Which filmmaker directed the movie Inception?",
        ["James Cameron", "Christopher Nolan", "David Fincher", "Denis Villeneuve"],
        1,
        "Christopher Nolan directed the science-fiction film Inception."
    ),

    (
        "Celebrities", "Easy",
        "Freddie Mercury was the lead singer of which famous rock band?",
        ["The Beatles", "Queen", "Pink Floyd", "The Rolling Stones"],
        1,
        "Freddie Mercury was the legendary lead vocalist of Queen."
    ),

    (
        "Celebrities", "Medium",
        "For which film did Leonardo DiCaprio win his first Academy Award for acting?",
        ["Titanic", "The Wolf of Wall Street", "The Revenant", "Inception"],
        2,
        "Leonardo DiCaprio won his first acting Oscar for The Revenant."
    ),

    (
        "Celebrities", "Medium",
        "Before her solo career, Beyoncé was a member of which girl group?",
        ["TLC", "The Pussycat Dolls", "Destiny's Child", "Fifth Harmony"],
        2,
        "Beyoncé was a member of Destiny's Child before becoming a solo artist."
    ),

    (
        "Celebrities", "Medium",
        "Which actor played Raj Malhotra in Dilwale Dulhania Le Jayenge?",
        ["Salman Khan", "Aamir Khan", "Shah Rukh Khan", "Saif Ali Khan"],
        2,
        "Shah Rukh Khan played Raj Malhotra in Dilwale Dulhania Le Jayenge."
    ),

    (
        "Celebrities", "Medium",
        "Which Indian actor is popularly known as 'Big B'?",
        ["Aamir Khan", "Amitabh Bachchan", "Anil Kapoor", "Dharmendra"],
        1,
        "Amitabh Bachchan is popularly known as Big B."
    ),

    (
        "Celebrities", "Medium",
        "Who directed the Indian film RRR?",
        ["Sanjay Leela Bhansali", "S. S. Rajamouli", "Rajkumar Hirani", "Mani Ratnam"],
        1,
        "S. S. Rajamouli directed the internationally acclaimed film RRR."
    ),

    (
        "Celebrities", "Hard",
        "Which actress played the title character in the Hindi film Piku?",
        ["Priyanka Chopra", "Alia Bhatt", "Deepika Padukone", "Kareena Kapoor"],
        2,
        "Deepika Padukone portrayed Piku Banerjee in the film Piku."
    ),

    (
        "Celebrities", "Hard",
        "Which actor portrays Wade Wilson, also known as Deadpool?",
        ["Ryan Gosling", "Ryan Reynolds", "Hugh Jackman", "Chris Pratt"],
        1,
        "Ryan Reynolds portrays Wade Wilson, also known as Deadpool."
    ),

    (
        "Celebrities", "Hard",
        "What is the name of Meryl Streep's character in The Devil Wears Prada?",
        ["Miranda Priestly", "Andrea Sachs", "Emily Charlton", "Nigel Kipling"],
        0,
        "Meryl Streep plays Miranda Priestly, the editor-in-chief of Runway magazine."
    ),

]


# ==================================================
# DATABASE INSERTION
# ==================================================

def seed_questions():

    db = SessionLocal()

    inserted_count = 0
    skipped_count = 0

    try:

        for item in questions_data:

            category_name = item[0]
            difficulty = item[1]
            question_text = item[2]
            options = item[3]
            correct_index = item[4]
            explanation = item[5]

            # Validate question structure
            if len(options) != 4:
                raise ValueError(
                    f"Question must have exactly 4 options: {question_text}"
                )

            if correct_index not in range(4):
                raise ValueError(
                    f"Invalid correct answer index: {question_text}"
                )

            # Find category
            category = db.query(Category).filter(
                Category.category_name == category_name
            ).first()

            if not category:
                raise ValueError(
                    f"Category not found: {category_name}"
                )

            # Skip duplicate questions
            existing_question = db.query(Question).filter(
                Question.category_id == category.category_id,
                Question.question_text == question_text
            ).first()

            if existing_question:
                print(f"Skipped duplicate: {question_text}")
                skipped_count += 1
                continue

            # Create question
            new_question = Question(
                category_id=category.category_id,
                question_text=question_text,
                difficulty=difficulty,
                explanation=explanation
            )

            db.add(new_question)
            db.flush()

            # Insert four options
            for index, option_text in enumerate(options):

                new_option = AnswerOption(
                    question_id=new_question.question_id,
                    option_text=option_text,
                    is_correct=(index == correct_index)
                )

                db.add(new_option)

            inserted_count += 1

            print(
                f"Added: {category_name} | "
                f"{difficulty} | {question_text}"
            )

        db.commit()

        print("\n====================================")
        print("QUIZFLIX BATCH 2 INSERTION COMPLETE")
        print("====================================")
        print(f"Questions inserted: {inserted_count}")
        print(f"Questions skipped: {skipped_count}")
        print(f"Questions in this batch: {len(questions_data)}")
        print(f"Total new answer options: {inserted_count * 4}")
        print("Database changes committed successfully!")

    except Exception as error:

        db.rollback()

        print("\nERROR: Database insertion failed.")
        print(error)

        raise

    finally:

        db.close()


if __name__ == "__main__":
    seed_questions()
