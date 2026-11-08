# QUIZFLIX
# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

**Project Name:** QuizFlix – Movie and Music Trivia Gaming Platform  
**Student Name:** Masoom Shaikh  
**Department:** Computer Science / Data Science  
**Document Version:** 1.0  
**Date:** 8 November 2026

---

# 1. INTRODUCTION

## 1.1 Purpose

The purpose of this Software Requirements Specification (SRS) document is to describe the functional and non-functional requirements of QuizFlix, an interactive entertainment trivia gaming platform.

QuizFlix enables users to participate in multiple-choice quizzes based on movies, music, web series and celebrities. The system provides user authentication, difficulty-based quizzes, automatic scoring, answer reviews, quiz history and leaderboard functionality.

This document describes the system's purpose, scope, user requirements, system features, interfaces, constraints and major technical requirements.

## 1.2 Project Scope

QuizFlix is a web-based trivia gaming application developed to provide an engaging platform for users to test and improve their entertainment knowledge.

The system includes:

- User registration and login.
- Secure password hashing and JWT-based authentication.
- Multiple entertainment categories.
- Easy, Medium and Hard quiz difficulty levels.
- Randomized question selection.
- Multiple-choice questions with four options.
- Server-side answer validation.
- Automatic score and accuracy calculation.
- Detailed answer review with explanations.
- Personal quiz history.
- Leaderboard and player rankings.
- Administrative category and question management.
- External entertainment content search using the Apple iTunes Search API.

The project also incorporates software engineering practices such as modular development, automated testing, Test-Driven Development, Git version control, data analysis, machine learning demonstrations and Continuous Integration.

## 1.3 Intended Audience

This document is intended for:

- Project developers.
- Software engineering faculty members.
- Project evaluators.
- Students and academic reviewers.
- Future developers who may maintain or extend QuizFlix.

## 1.4 Definitions and Abbreviations

| Term | Description |
|---|---|
| SRS | Software Requirements Specification |
| API | Application Programming Interface |
| JWT | JSON Web Token |
| CRUD | Create, Read, Update and Delete |
| DBMS | Database Management System |
| UI | User Interface |
| SQL | Structured Query Language |
| CI | Continuous Integration |
| ORM | Object Relational Mapping |

---

# 2. OVERALL DESCRIPTION

## 2.1 Product Perspective

QuizFlix is a web-based application following a client-server architecture.

The frontend provides the user interface through which users register, log in, select quizzes, answer questions and view results.

The backend is developed using FastAPI and handles authentication, business logic, quiz management, score calculation and database operations.

MySQL is used for persistent storage, while SQLAlchemy provides database interaction through an ORM.

The system also integrates an external entertainment metadata API for movie, music and television content searches.

## 2.2 Product Functions

The major functions of QuizFlix include:

1. User account registration.
2. User authentication and authorization.
3. Category selection.
4. Difficulty selection.
5. Randomized quiz generation.
6. Question and answer presentation.
7. Answer submission and validation.
8. Automatic score calculation.
9. Answer review and explanation.
10. Quiz history retrieval.
11. Leaderboard generation.
12. Administrative content management.
13. External entertainment metadata search.

## 2.3 User Classes and Characteristics

### A. General User / Player

A player can:

- Register an account.
- Log in to the application.
- View available quiz categories.
- Select quiz difficulty.
- Participate in quizzes.
- Submit answers.
- View scores and accuracy.
- Review correct and incorrect answers.
- Access personal quiz history.
- View the leaderboard.

### B. Administrator

An administrator is responsible for managing application content.

Administrative capabilities include:

- Creating quiz categories.
- Updating categories.
- Deleting categories when no questions are associated with them.
- Creating and managing quiz questions.
- Managing answer options.
- Maintaining question correctness information.

Administrative endpoints require administrator authorization.

## 2.4 Operating Environment

| Component | Technology |
|---|---|
| Operating System | Windows |
| Frontend | HTML, CSS and JavaScript |
| Backend Language | Python |
| Backend Framework | FastAPI |
| Database | MySQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Password Hashing | Passlib and bcrypt |
| External API | Apple iTunes Search API |
| Testing Framework | Pytest |
| Version Control | Git and GitHub |
| CI Platform | GitHub Actions |

## 2.5 Design and Implementation Constraints

The following constraints apply:

- The application requires a Python environment for backend execution.
- MySQL must be configured for persistent application data.
- Database credentials and secret keys must be stored in environment variables.
- The backend exposes REST API endpoints.
- The frontend communicates with the backend through HTTP requests.
- External API availability depends on the third-party service.
- The external API integration uses request timeouts and error handling.
- The current machine-learning demonstration uses simulated quiz-performance data.

## 2.6 Assumptions and Dependencies

- Users have access to a modern web browser.
- The backend and MySQL database are available during application usage.
- Users provide valid registration information.
- The external iTunes Search API is accessible when external searches are performed.
- Internet connectivity is required for GitHub operations and external API searches.

---

# 3. FUNCTIONAL REQUIREMENTS

## FR-01: User Registration

The system shall allow new users to create an account by providing a username, email address and password.

The system shall:

- Validate registration information.
- Reject duplicate email addresses.
- Reject duplicate usernames.
- Hash passwords before storing them.
- Reject passwords exceeding the configured bcrypt byte limit.

## FR-02: User Login

The system shall allow registered users to authenticate using their email address and password.

The system shall:

- Verify the supplied password against the stored password hash.
- Reject invalid credentials.
- Generate a JWT access token after successful authentication.
- Return the token using bearer-token authentication.

## FR-03: User Profile

The system shall provide an authenticated endpoint that retrieves information about the currently logged-in user.

## FR-04: Category Management

The system shall provide entertainment categories for quiz participation.

The current categories include:

- Movies.
- Music.
- Web Series.
- Celebrities.

Administrators shall be able to create, retrieve, update and delete categories according to the implemented authorization and validation rules.

## FR-05: Question Management

The system shall support the creation and retrieval of quiz questions associated with categories and difficulty levels.

Each question shall have associated answer options.

## FR-06: Quiz Initiation

The system shall allow authenticated users to start a quiz by selecting:

- A category.
- A difficulty level.
- The number of questions.

The system shall randomly select questions matching the requested category and difficulty.

The system shall reject a request when the selected category does not exist or insufficient questions are available.

## FR-07: Multiple-Choice Questions

Each quiz question shall present four answer options.

The correct answer shall not be exposed in the quiz-start response.

## FR-08: Answer Submission

The system shall allow users to submit their selected answer options.

The backend shall validate:

- Quiz attempt ownership.
- Quiz completion status.
- Number of submitted answers.
- Duplicate question submissions.
- Question assignment to the quiz attempt.
- Validity of selected answer options.

## FR-09: Score Calculation

The system shall calculate quiz scores according to the implemented scoring logic.

Each correct answer contributes 10 points.

Score = Number of Correct Answers × 10

Accuracy is calculated as:

Accuracy (%) = (Correct Answers / Total Questions) × 100

## FR-10: Quiz Results and Answer Review

After submission, the system shall generate a result containing:

- Total questions.
- Correct answers.
- Score.
- Accuracy.
- Completion status.
- Selected answers.
- Correct answers.
- Explanations for questions where available.

## FR-11: Quiz History

The system shall allow authenticated users to retrieve their previous quiz attempts.

Users shall only retrieve their own quiz history.

## FR-12: Leaderboard

The system shall provide a leaderboard based on aggregated quiz performance.

The leaderboard shall display player rankings and relevant performance information.

## FR-13: External API Integration

The system shall support external entertainment content searches through the Apple iTunes Search API.

Supported search types include:

- Movies.
- Music.
- Television shows.

The system shall process JSON responses and handle invalid inputs, network errors, request timeouts and invalid JSON responses.

## FR-14: Authentication and Authorization

The system shall protect authenticated endpoints using JWT-based authentication.

Administrator operations shall require administrator authorization.

---

# 4. NON-FUNCTIONAL REQUIREMENTS

## 4.1 Performance Requirements

- The application should respond within a reasonable time under normal usage.
- Quiz questions should be retrieved efficiently.
- The backend should support multiple concurrent requests.
- API response times should be measurable through performance testing.
- Error rates and throughput should be evaluated under the tested conditions.

## 4.2 Security Requirements

- Passwords must never be stored in plain text.
- JWT authentication must protect authenticated endpoints.
- Administrator functions must be protected.
- Database credentials must not be exposed in the source repository.
- Users must not access other users' quiz attempts.
- Submitted answer options must be validated by the backend.

## 4.3 Reliability Requirements

- The system should handle invalid user input gracefully.
- External API failures should produce appropriate error responses.
- Completed quiz attempts must not be submitted again.
- Database operations should use appropriate transaction handling.

## 4.4 Usability Requirements

- The application should provide a clear and understandable user interface.
- Quiz categories and difficulty levels should be easy to identify.
- Results and answer explanations should be presented clearly.
- Users should be able to navigate between the dashboard, quiz and result pages.

## 4.5 Maintainability Requirements

- Backend components should be organized into models, routers, schemas and services.
- Functional code should be modular.
- Dependencies should be documented in requirements.txt.
- Automated tests should help detect regressions.
- Git and GitHub should be used for version control.

---

# 5. EXTERNAL INTERFACE REQUIREMENTS

## 5.1 User Interface

The frontend consists of the following pages:

| Page | Purpose |
|---|---|
| Login | User authentication |
| Registration | New account creation |
| Dashboard | Categories, profile and leaderboard |
| Quiz | Display questions and answer options |
| Result | Display score and answer review |

## 5.2 Software Interfaces

The application interacts with:

- FastAPI backend services.
- MySQL database.
- SQLAlchemy ORM.
- Apple iTunes Search API.
- Browser-based JavaScript fetch operations.
- GitHub Actions for automated testing.

## 5.3 Communication Interfaces

The frontend communicates with the backend through HTTP requests.

The backend exposes REST-style endpoints and returns JSON responses.

The external API integration uses HTTPS requests through Python Requests.

---

# 6. DATABASE REQUIREMENTS

The system uses MySQL as its primary relational database.

The database contains entities supporting:

- User accounts.
- Categories.
- Questions.
- Answer options.
- Quiz attempts.
- User answers.
- Questions assigned to quiz attempts.

Primary keys and foreign-key relationships maintain data associations.

Passwords are stored as hashes rather than plain-text values.

Quiz attempts and submitted answers are persisted for result generation and history retrieval.

---

# 7. SYSTEM ARCHITECTURE

QuizFlix follows a layered client-server architecture.

### Presentation Layer

Contains HTML, CSS and JavaScript files responsible for user interaction.

### Application Layer

Contains FastAPI routers, request validation and application logic.

### Service Layer

Contains authentication, scoring and external API services.

### Data Layer

Uses SQLAlchemy and MySQL to store and retrieve application data.

### External Service Layer

Connects to the Apple iTunes Search API to retrieve entertainment metadata.

---

# 8. SYSTEM TESTING AND VALIDATION

The application uses Pytest for automated testing.

The current automated test suite covers:

- Authentication.
- Registration validation.
- Quiz creation.
- Quiz answer submission.
- Scoring.
- Test-Driven Development.
- External API handling.
- CRUD operations.
- Quiz history.

The latest locally verified execution recorded:

**44 tests passed, 0 failed.**

The GitHub Actions CI workflow also successfully executed all 44 tests remotely.

Performance testing has been performed using sequential and concurrent HTTP requests.

Functional and performance testing reports are maintained in the project's documentation folder.

---

# 9. LIMITATIONS AND FUTURE ENHANCEMENTS

Potential future improvements include:

- Increasing the size and diversity of the question bank.
- Adding more entertainment metadata providers.
- Implementing additional administrative dashboards.
- Adding richer user profile statistics.
- Introducing advanced recommendation features.
- Improving production-scale performance.
- Expanding frontend and accessibility testing.

The current data science and machine-learning components are academic demonstrations based on simulated quiz-performance data.

---

# 10. CONCLUSION

QuizFlix is designed as an interactive entertainment trivia platform that combines web development, database management, authentication, external API integration and automated testing.

This SRS document establishes the functional and non-functional requirements of the system and provides a reference for implementation, testing, maintenance and future development.

**End of Document**