# QUIZFLIX
# LAB 7 - FUNCTIONAL TESTING REPORT

**Project:** QuizFlix - Movie and Music Trivia Gaming Platform  
**Student:** Masoom Shaikh  
**Testing Framework:** Pytest  
**Backend:** FastAPI  
**Database:** MySQL (application database)  
**Testing Database:** Temporary SQLite database for automated API tests  
**Frontend:** HTML, CSS and JavaScript  
**Browser:** Google Chrome  
**Testing Date:** 8 November 2026  
**Report Version:** 2.0

---

# 1. INTRODUCTION

Functional testing is performed to verify that the QuizFlix application behaves according to its functional requirements.

The purpose of this testing is to ensure that users can register, log in, select quiz categories, start quizzes, submit answers, receive results and access their quiz history.

It also verifies that the application correctly handles invalid inputs, unauthorized requests and unexpected situations.

In addition to automated API testing, browser-level testing was performed to verify the actual user interface and application workflows.

# 2. OBJECTIVES

The main objectives are:

1. Verify user registration and authentication.
2. Verify quiz category and difficulty selection.
3. Verify quiz creation and question selection.
4. Validate submitted answers.
5. Verify automatic score and accuracy calculation.
6. Verify quiz result generation and answer review.
7. Verify quiz history retrieval and display.
8. Test leaderboard functionality.
9. Verify logout and protected dashboard access.
10. Test invalid inputs and error handling.
11. Verify external API integration.
12. Ensure that users cannot access another user's quiz attempts.

# 3. TESTING ENVIRONMENT

| Component | Details |
|---|---|
| Operating System | Windows |
| Programming Language | Python 3.13.7 |
| Backend Framework | FastAPI |
| Application Database | MySQL |
| ORM | SQLAlchemy |
| Testing Framework | Pytest 9.2.0 |
| API Testing | FastAPI TestClient |
| Test Database | In-memory SQLite |
| Frontend | HTML, CSS, JavaScript |
| Browser | Google Chrome |
| API Documentation | FastAPI Swagger UI |
| Version Control | Git and GitHub |

**Database clarification:** MySQL is used as the application's primary persistent database. Automated API tests use an isolated temporary SQLite database through test configuration and dependency overrides.

# 4. AUTOMATED FUNCTIONAL TEST CASES

The following automated test cases cover the main functional requirements of QuizFlix.

## 4.1 User Registration and Authentication

| Test ID | Test Scenario | Test Input / Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| FT01 | Successful registration | Submit valid username, email and password | User account created successfully | HTTP 201 returned and user saved | PASS |
| FT02 | Duplicate email | Register using an existing email | Registration rejected | HTTP 409 returned | PASS |
| FT03 | Duplicate username | Register using an existing username | Registration rejected | HTTP 409 returned | PASS |
| FT04 | Excessively long password | Submit a password exceeding 72 UTF-8 bytes | Registration rejected | HTTP 400 returned | PASS |
| FT05 | Successful login | Submit registered email and correct password | JWT access token generated | HTTP 200 and bearer token returned | PASS |
| FT06 | Incorrect password | Submit correct email with incorrect password | Login rejected | HTTP 401 returned | PASS |
| FT07 | Unknown email | Submit an email not registered in the system | Login rejected | HTTP 401 returned | PASS |

## 4.2 Quiz Management and Submission

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

## 4.3 External API Integration

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| FT18 | Search entertainment content | External API returns structured JSON | Successful response received | PASS |
| FT19 | Empty search query | Request rejected | HTTP 400 returned | PASS |
| FT20 | Invalid media type | Request rejected | HTTP 422 returned | PASS |
| FT21 | Invalid result limit | Request rejected | HTTP 422 returned | PASS |
| FT22 | External API timeout | Timeout handled gracefully | HTTP 504 returned in simulated test | PASS |
| FT23 | External API connection failure | Connection error handled gracefully | HTTP 502 returned in simulated test | PASS |
| FT24 | Invalid JSON response | Invalid response handled gracefully | HTTP 502 returned in simulated test | PASS |

## 4.4 CRUD Operations Testing

The CRUD operations were tested using the API testing environment.

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| FT25 | Retrieve categories using GET | Categories returned successfully | HTTP 200 returned | PASS |
| FT26 | Create category using POST | New category created | HTTP 201 returned | PASS |
| FT27 | Update category using PUT | Category updated successfully | HTTP 200 returned | PASS |
| FT28 | Delete category using DELETE | Category deleted successfully | HTTP 200 returned | PASS |
| FT29 | Use unsupported PATCH method | Request rejected | HTTP 405 returned | PASS |

# 5. MANUAL BROWSER-LEVEL FUNCTIONAL TESTING

Manual browser-level testing was performed using Google Chrome to verify the actual QuizFlix frontend and its interaction with the backend.

The application was accessed through the local frontend server and FastAPI backend.

## 5.1 Login and Dashboard Testing

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| MB01 | Open login page | Login interface loads correctly | Login page loaded with email and password fields | PASS |
| MB02 | Login using an existing account | User authenticated and redirected to dashboard | Dashboard opened successfully | PASS |
| MB03 | Dashboard loading | Username, statistics and categories displayed | Dashboard information displayed correctly | PASS |

## 5.2 Category and Quiz Testing

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| MB04 | Navigate to Movies category | Category selection works | Movies category opened successfully | PASS |
| MB05 | Select Easy difficulty | Quiz starts with selected difficulty | Quiz started successfully | PASS |
| MB06 | Load quiz interface | Questions and answer options displayed | Question and four answer options displayed | PASS |
| MB07 | Select and submit answers | Answers accepted and result generated | Quiz submitted successfully | PASS |
| MB08 | Display quiz score | Correct score and accuracy displayed | 40 points and 100% accuracy displayed for four correct answers | PASS |
| MB09 | Display answer review | Selected and correct answers displayed | Answer review and available explanations displayed | PASS |
| MB10 | Return to dashboard | Dashboard opened from result page | Dashboard opened successfully | PASS |

## 5.3 Dashboard and Leaderboard Testing

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| MB11 | Update dashboard statistics | Statistics reflect completed quiz attempts | Quiz count and total score updated | PASS |
| MB12 | Open leaderboard | Leaderboard displays player rankings | Player names, scores, quiz counts and accuracy displayed | PASS |

## 5.4 Quiz History Interface Testing

The Quiz History interface was added to the dashboard to allow users to view their previous quiz attempts.

The backend history endpoint was already implemented and was used to retrieve the records.

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| MB13 | Retrieve history through API | Previous attempts returned | HTTP 200 and quiz history returned in Swagger UI | PASS |
| MB14 | Display Quiz History interface | Previous attempts displayed in dashboard | History table displayed successfully | PASS |
| MB15 | Display attempt details | Attempt ID, category, difficulty, score, correct answers, accuracy, status and date displayed | Attempt information displayed correctly | PASS |
| MB16 | Refresh Quiz History | Latest attempts retrieved again | New quiz attempt appeared after refreshing | PASS |

## 5.5 Logout and Access Control Testing

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| MB17 | Logout | User logged out and redirected to login | Login page displayed | PASS |
| MB18 | Access dashboard after logout | Unauthenticated user redirected to login | Login page displayed automatically | PASS |

## 5.6 Registration and New User Login Testing

During browser-level testing, the registration link initially did not navigate to the registration page because it used a placeholder link.

The navigation was corrected to point directly to `register.html`.

The registration and new-user login workflows were then tested again.

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| MB19 | Open registration page | Registration page opens from login page | Registration page opened successfully after navigation correction | PASS |
| MB20 | Register a new user | New user account created | Registration completed successfully | PASS |
| MB21 | Login using new account | Newly registered user authenticated | Login successful and dashboard opened | PASS |

## 5.7 Testing All Entertainment Categories

All four entertainment categories were tested through the browser.

| Test ID | Category | Test Scenario | Actual Result | Status |
|---|---|---|---|---|
| MB22 | Movies | Start and complete a quiz | Quiz functionality worked successfully | PASS |
| MB23 | Music | Start and complete a quiz | Quiz functionality worked successfully | PASS |
| MB24 | Web Series | Start and complete a quiz | Quiz functionality worked successfully | PASS |
| MB25 | Celebrities | Start and complete a quiz | Quiz functionality worked successfully | PASS |

Quiz attempts from the tested categories were also visible in the Quiz History section.

# 6. AUTOMATED TEST EXECUTION SUMMARY

The automated test suite was executed using:

```bash
python -m pytest -v
```

The latest verified execution produced the following results:

| Test Module | Automated Tests Passed |
|---|---:|
| `test_auth.py` | 7 |
| `test_crud_methods.py` | 5 |
| `test_external_api.py` | 8 |
| `test_quizzes.py` | 10 |
| `test_scoring.py` | 11 |
| `test_tdd_scoring.py` | 3 |
| **Total** | **44** |

The 29 numbered functional test cases in Section 4 describe the main testing scenarios. Some tests use parameterized inputs, and the complete automated suite also includes additional scoring and TDD tests. Therefore, the number of collected automated test executions is 44.

## 6.1 Final Automated Test Results

| Result | Count |
|---|---:|
| Tests Collected | 44 |
| Passed | 44 |
| Failed | 0 |
| Warnings | 1 |
| Execution Time | 7.91 seconds |

<badge color="success">44 Passed, 0 Failed</badge>

The test execution completed successfully.

One non-fatal Starlette deprecation warning involving HTTPX and the test client was reported. The warning did not cause any test failures.

## 6.2 Continuous Integration Verification

The project's GitHub Actions CI workflow was also successfully executed.

The verified workflow completed the automated test suite with:

- 44 tests passed.
- 0 failed tests.
- Successful workflow execution.

This verifies that the automated test suite can also be executed through the configured GitHub Actions workflow.

# 7. IMPORTANT TESTING OBSERVATIONS

The following observations were recorded during functional testing:

1. Passwords are hashed before being stored in the database.
2. Duplicate email addresses and usernames are rejected.
3. Invalid authentication attempts are rejected.
4. Correct answers are not exposed when a quiz starts.
5. Submitted question IDs must match the questions assigned to the attempt.
6. Answer options must belong to their respective questions.
7. Completed quiz attempts cannot be submitted again.
8. Scoring and accuracy calculations are validated through automated tests.
9. External API timeouts, connection failures and invalid JSON responses are handled.
10. Dashboard statistics update after quiz completion.
11. The leaderboard successfully displays player rankings.
12. Quiz History retrieves and displays previous quiz attempts.
13. The Refresh History button retrieves updated quiz records.
14. Logout removes the authentication token from the frontend session.
15. Unauthenticated users are redirected away from the dashboard.
16. All four entertainment categories were tested through the browser.
17. New user registration and login were successfully verified.

# 8. TESTING LIMITATIONS

The automated API tests use an isolated in-memory SQLite database. They do not represent a complete failure simulation of the MySQL database.

The external API failure tests use mocked responses to simulate timeouts, connection errors and invalid JSON.

Manual browser-level testing was performed in a local development environment. It does not represent a full production deployment or large-scale user testing.

Additional testing could include database outage simulation, security penetration testing, broader browser compatibility checks and production-scale load testing.

# 9. CONCLUSION

Functional testing was performed to verify that the major QuizFlix features operate according to their implemented requirements.

Automated testing using Pytest verified authentication, quiz creation, answer submission, scoring, CRUD operations, external API handling and quiz history retrieval.

Manual browser-level testing verified login, registration, dashboard navigation, all four entertainment categories, quiz participation, result generation, answer review, dashboard statistics, leaderboard, Quiz History, logout and protected dashboard access.

The latest automated test execution recorded 44 passing tests with zero failures.

The browser-level testing also confirmed successful completion of the main user workflows in the local development environment.

Therefore, the tested QuizFlix functionality has successfully passed the documented automated and manual functional testing scenarios.

---

**END OF FUNCTIONAL TESTING REPORT**