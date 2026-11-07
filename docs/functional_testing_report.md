
# QUIZFLIX
## Lab 7 – Functional Testing Report

**Project:** QuizFlix – Movie and Music Trivia Gaming Platform  
**Student:** Masoom Shaikh  
**Testing Framework:** Pytest  
**Backend:** FastAPI  
**Database:** MySQL (application database)  
**Testing Database:** Temporary SQLite database for automated API tests  
**Testing Date:** 7 November 2026  

---

## 1. Introduction

Functional testing is performed to verify that the QuizFlix application behaves according to its functional requirements.

The purpose of this testing is to ensure that users can register, log in, select quiz categories, start quizzes, submit answers, receive results and access their quiz history.

It also verifies that the application correctly handles invalid inputs, unauthorized requests and unexpected situations.

## 2. Objectives

The main objectives are:

1. Verify user registration and authentication.
2. Verify quiz category and difficulty selection.
3. Verify quiz creation and question selection.
4. Validate submitted answers.
5. Verify automatic score and accuracy calculation.
6. Verify quiz result generation and answer review.
7. Verify quiz history retrieval.
8. Test invalid inputs and error handling.
9. Ensure that users cannot access another user's quiz attempts.

## 3. Testing Environment

| Component | Details |
|---|---|
| Operating System | Windows 11 |
| Programming Language | Python 3.13.7 |
| Backend Framework | FastAPI |
| Database | MySQL |
| ORM | SQLAlchemy |
| Testing Framework | Pytest 9.2.0 |
| API Testing | FastAPI TestClient |
| Test Database | In-memory SQLite |
| Frontend | HTML, CSS, JavaScript |
| Browser | Google Chrome |

## 4. Functional Test Cases

The following test cases cover the main functional requirements of QuizFlix.

### 4.1 User Registration and Authentication

| Test ID | Test Scenario | Test Input / Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| FT01 | Successful registration | Submit valid username, email and password | User account created successfully | HTTP 201 returned and user saved | PASS |
| FT02 | Duplicate email | Register using an existing email | Registration rejected | HTTP 409 returned | PASS |
| FT03 | Duplicate username | Register using an existing username | Registration rejected | HTTP 409 returned | PASS |
| FT04 | Excessively long password | Submit a password exceeding 72 UTF-8 bytes | Registration rejected | HTTP 400 returned | PASS |
| FT05 | Successful login | Submit registered email and correct password | JWT access token generated | HTTP 200 and bearer token returned | PASS |
| FT06 | Incorrect password | Submit correct email with incorrect password | Login rejected | HTTP 401 returned | PASS |
| FT07 | Unknown email | Submit an email not registered in the system | Login rejected | HTTP 401 returned | PASS |

### 4.2 Quiz Management and Submission

| Test ID | Test Scenario | Test Input / Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| FT08 | Start quiz | Select an existing category, difficulty and valid question count | Quiz attempt created | HTTP 201 returned with assigned questions | PASS |
| FT09 | Invalid category | Submit a non-existing category ID | Quiz creation rejected | HTTP 404 returned | PASS |
| FT10 | Insufficient questions | Request more questions than available | Quiz creation rejected | HTTP 400 returned | PASS |
| FT11 | Submit all correct answers | Submit the correct options for all assigned questions | Full score generated | 20 points and 100% accuracy for the two-question test | PASS |
| FT12 | Submit incomplete answers | Submit fewer answers than required | Submission rejected | HTTP 400 returned | PASS |
| FT13 | Duplicate question answers | Submit duplicate question IDs | Submission rejected | HTTP 400 returned | PASS |
| FT14 | Unassigned question | Submit a question not assigned to the attempt | Submission rejected | HTTP 400 returned | PASS |
| FT15 | Invalid answer option | Submit an option belonging to another question | Submission rejected | HTTP 400 returned | PASS |
| FT16 | Resubmit completed quiz | Submit answers to an already completed attempt | Repeat submission rejected | HTTP 400 returned | PASS |
| FT17 | Retrieve quiz history | Request the authenticated user's quiz history | Previous quiz attempts returned | HTTP 200 returned with saved quiz history | PASS |

### 4.3 External API Integration

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| FT18 | Search entertainment content | External API returns structured JSON | Successful response received | PASS |
| FT19 | Empty search query | Request rejected | HTTP 400 returned | PASS |
| FT20 | Invalid media type | Request rejected | HTTP 422 returned | PASS |
| FT21 | Invalid result limit | Request rejected | HTTP 422 returned | PASS |
| FT22 | External API timeout | Timeout handled gracefully | HTTP 504 returned in simulated test | PASS |
| FT23 | External API connection failure | Connection error handled gracefully | HTTP 502 returned in simulated test | PASS |
| FT24 | Invalid JSON response | Invalid response handled gracefully | HTTP 502 returned in simulated test | PASS |

## 5. Test Execution Summary

The automated test suite was executed using:

```bash
python -m pytest -v
```

The latest verified execution produced the following results:

| Testing Module | Test Cases Passed |
|---|---:|
| Authentication Testing | 7 |
| External API Testing | 8 |
| Quiz API Testing | 10 |
| Scoring Testing | 11 |
| TDD Accuracy Testing | 3 |
| **Total** | **39** |

**Final Result: 39 Passed, 0 Failed**

Execution time: 4.52 seconds.

## 6. Important Testing Observations

1. Passwords are hashed before being stored in the database.
2. Duplicate email addresses and usernames are rejected.
3. Invalid authentication attempts are rejected.
4. Correct answers are not exposed when a quiz starts.
5. Submitted question IDs must match the questions assigned to the attempt.
6. Answer options must belong to their respective questions.
7. Completed quiz attempts cannot be submitted again.
8. Scoring and accuracy calculations are validated through automated tests.
9. External API timeouts, connection failures and invalid JSON responses are handled.

## 7. Testing Limitations

The automated API tests use an isolated in-memory SQLite database. They do not represent a complete failure simulation of the production MySQL database.

The external API failure tests use mocked responses to simulate timeouts, connection errors and invalid JSON.

Manual browser-level acceptance testing, database outage testing and some frontend interaction scenarios require separate verification.

## 8. Conclusion

Functional and automated API testing demonstrates that the major QuizFlix backend features behave according to their implemented requirements.

The application successfully supports user authentication, quiz creation, answer submission, score calculation, result generation, quiz history and external entertainment searches.

The automated test suite achieved 39 passing tests with no failures in its latest verified execution.

Therefore, the implemented core functionality has passed the current automated testing scenarios.
