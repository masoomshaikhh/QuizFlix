# QUIZFLIX
# LAB 8 - PERFORMANCE TESTING AND API TESTING REPORT

**Project:** QuizFlix - Movie and Music Trivia Gaming Platform
**Student:** Masoom Shaikh
**Programming Language:** Python 3.13.7
**Backend Framework:** FastAPI
**Database:** MySQL
**Testing Libraries:** Requests, Pandas, NumPy, Pytest
**Testing Environment:** Windows
**Testing Date:** 7 November 2026

---

## 1. INTRODUCTION

Performance testing and API testing are important software testing activities used to evaluate the responsiveness, reliability and behaviour of an application.

In QuizFlix, performance testing was conducted to measure API response times, throughput, error rates and the behaviour of endpoints under sequential and concurrent requests.

API testing was also performed to verify HTTP methods, status codes and JSON responses.

The testing focused on the following endpoints:

- `/health`
- `/api/leaderboard/`

## 2. OBJECTIVES

The main objectives of this lab are:

1. Measure API response times.
2. Calculate minimum, maximum and average response times.
3. Measure API throughput.
4. Calculate request failure and error rates.
5. Perform sequential request testing.
6. Perform concurrent request testing.
7. Test HTTP methods such as GET, POST, PUT, PATCH and DELETE.
8. Verify HTTP status codes and JSON responses.
9. Evaluate API behaviour under multiple requests.

## 3. TESTING ENVIRONMENT

| Component | Details |
|---|---|
| Operating System | Windows |
| Programming Language | Python 3.13.7 |
| Backend Framework | FastAPI |
| Database | MySQL |
| HTTP Library | Requests 2.34.2 |
| Data Analysis | Pandas and NumPy |
| Automated Testing | Pytest 9.2.0 |
| Concurrent Testing | ThreadPoolExecutor |
| Development Server | Uvicorn |
| Local Backend | http://127.0.0.1:8000 |

## 4. PERFORMANCE TESTING METHODOLOGY

Performance testing was performed using a custom Python script named:

`run_performance.py`

The script measures the performance of two QuizFlix API endpoints.

**Endpoint 1: Health Check**

`GET /health`

This endpoint verifies whether the QuizFlix backend is running successfully.

**Endpoint 2: Leaderboard**

`GET /api/leaderboard/`

This endpoint retrieves leaderboard information from the application database.

### Testing Configuration

| Parameter | Value |
|---|---:|
| Requests per test | 100 |
| Concurrent workers | 10 |
| Sequential tests | 2 |
| Concurrent tests | 2 |
| Total GET requests | 400 |
| Request timeout | 15 seconds |

### Testing Types

**Sequential Testing**

Requests are sent one after another. The response time of each request is recorded.

**Concurrent Testing**

Multiple requests are executed simultaneously using Python's ThreadPoolExecutor with 10 worker threads.

## 5. PERFORMANCE METRICS

The following metrics were calculated:

**Minimum Response Time:** The shortest recorded request response time.

**Maximum Response Time:** The longest recorded request response time.

**Average Response Time:** The arithmetic mean of all recorded request response times.

**Median Response Time:** The middle value of the recorded response times.

**95th Percentile (P95):** The response time within which 95% of the recorded requests completed.

**Throughput:** The number of requests processed per second.

Formula:

Throughput = Total Requests / Total Execution Time

**Error Rate:**

Error Rate (%) = (Failed Requests / Total Requests) x 100

## 6. SEQUENTIAL PERFORMANCE TESTING RESULTS

A total of 100 sequential requests were sent to each endpoint.

### 6.1 Health Endpoint

Endpoint: `/health`

| Metric | Result |
|---|---:|
| Total Requests | 100 |
| Successful Requests | 100 |
| Failed Requests | 0 |
| Error Rate | 0% |
| Minimum Response Time | 2.94 ms |
| Maximum Response Time | 35.21 ms |
| Average Response Time | 19.63 ms |
| Median Response Time | 17.21 ms |
| P95 Response Time | 27.97 ms |
| Throughput | 50.46 requests/second |
| Total Execution Time | 1.98 seconds |

### 6.2 Leaderboard Endpoint

Endpoint: `/api/leaderboard/`

| Metric | Result |
|---|---:|
| Total Requests | 100 |
| Successful Requests | 100 |
| Failed Requests | 0 |
| Error Rate | 0% |
| Minimum Response Time | 5.96 ms |
| Maximum Response Time | 150.17 ms |
| Average Response Time | 24.39 ms |
| Median Response Time | 23.94 ms |
| P95 Response Time | 35.61 ms |
| Throughput | 40.71 requests/second |
| Total Execution Time | 2.46 seconds |

## 7. CONCURRENT PERFORMANCE TESTING RESULTS

Concurrent testing was performed using 10 worker threads with 100 requests per endpoint.

### 7.1 Health Endpoint

Endpoint: `/health`

| Metric | Result |
|---|---:|
| Total Requests | 100 |
| Successful Requests | 100 |
| Failed Requests | 0 |
| Error Rate | 0% |
| Minimum Response Time | 5.34 ms |
| Maximum Response Time | 23.06 ms |
| Average Response Time | 11.13 ms |
| Median Response Time | 10.76 ms |
| P95 Response Time | 18.89 ms |
| Throughput | 736.40 requests/second |
| Total Execution Time | 0.14 seconds |

### 7.2 Leaderboard Endpoint

Endpoint: `/api/leaderboard/`

| Metric | Result |
|---|---:|
| Total Requests | 100 |
| Successful Requests | 100 |
| Failed Requests | 0 |
| Error Rate | 0% |
| Minimum Response Time | 21.81 ms |
| Maximum Response Time | 246.33 ms |
| Average Response Time | 69.86 ms |
| Median Response Time | 49.46 ms |
| P95 Response Time | 217.60 ms |
| Throughput | 138.82 requests/second |
| Total Execution Time | 0.72 seconds |

## 8. SEQUENTIAL AND CONCURRENT PERFORMANCE COMPARISON

| Endpoint | Sequential Average | Concurrent Average |
|---|---:|---:|
| Health | 19.63 ms | 11.13 ms |
| Leaderboard | 24.39 ms | 69.86 ms |

### Observations

1. Both endpoints successfully processed all 100 sequential requests.
2. Both endpoints successfully processed all 100 concurrent requests.
3. No failed requests were recorded during either performance test.
4. The health endpoint demonstrated lower average response time during concurrent testing.
5. The leaderboard endpoint experienced higher response times under concurrent load. This may reflect the additional work involved in retrieving and processing leaderboard information.
6. The leaderboard's maximum concurrent response time was 246.33 ms.

The results represent measurements from a local development environment and a single test execution.

## 9. HTTP METHOD TESTING

HTTP method testing was initially performed against the `/health` endpoint to verify its supported methods and response handling.

### Results

| HTTP Method | Status Code | JSON Response | Result |
|---|---:|---|---|
| GET | 200 | Valid | PASS |
| POST | 405 | Valid | PASS |
| PUT | 405 | Valid | PASS |
| PATCH | 405 | Valid | PASS |
| DELETE | 405 | Valid | PASS |

**Explanation:**

The `/health` endpoint only supports GET requests. Therefore, POST, PUT, PATCH and DELETE correctly returned HTTP 405 (Method Not Allowed).

These results do not indicate that the other HTTP methods are unavailable throughout the QuizFlix application.

## 10. CRUD API METHOD TESTING

To further verify the application's CRUD functionality, automated tests were executed against the category API using a temporary in-memory SQLite database.

This prevented the tests from modifying the actual QuizFlix MySQL database.

The test file was:

`backend/tests/test_crud_methods.py`

### CRUD Test Results

| Test ID | HTTP Method | Operation | Expected Status | Actual Status | Result |
|---|---|---|---:|---:|---|
| API01 | GET | Retrieve categories | 200 | 200 | PASS |
| API02 | POST | Create category | 201 | 201 | PASS |
| API03 | PUT | Update category | 200 | 200 | PASS |
| API04 | DELETE | Delete category | 200 | 200 | PASS |
| API05 | PATCH | Test unsupported method | 405 | 405 | PASS |

### Observations

- GET successfully retrieved categories.
- POST successfully created a temporary category.
- PUT successfully updated the category.
- DELETE successfully removed the temporary category.
- PATCH returned HTTP 405 because it is not implemented in the category router.

All five automated CRUD tests passed.

## 11. AUTOMATED TEST EXECUTION

The CRUD API tests were executed using:

```bash
python -m pytest backend/tests/test_crud_methods.py -v -s
```

**Execution Result:**

- Total tests: 5
- Passed: 5
- Failed: 0
- Execution time: 1.65 seconds

## 12. GENERATED OUTPUT FILES

The performance testing script generated:

1. `performance_results.csv`
2. `http_method_results.csv`

These files contain the recorded performance measurements and HTTP method results.

The Python script used for performance testing is:

`backend/analytics/run_performance.py`

The CRUD testing script is:

`backend/tests/test_crud_methods.py`

## 13. LIMITATIONS

1. Performance tests were conducted on a local development environment rather than a production server.
2. Only two read-only endpoints were used for sequential and concurrent performance measurements.
3. The tests were conducted with 100 requests per endpoint and 10 concurrent workers.
4. The results represent one test execution and may vary between runs.
5. The CRUD tests used a temporary SQLite database rather than the actual MySQL database.
6. The PATCH method is not currently implemented in the category API.

Therefore, these results should not be interpreted as production-scale capacity measurements.

## 14. CONCLUSION

Performance and API testing were successfully conducted for the QuizFlix application.

Both the health check and leaderboard endpoints processed 100 sequential requests and 100 concurrent requests without any failed requests during the recorded tests.

Response times, throughput, minimum and maximum latency, median response time, 95th percentile response time and error rates were calculated.

The HTTP method testing verified the behaviour of GET, POST, PUT, PATCH and DELETE requests. Additional CRUD testing confirmed the successful creation, retrieval, updating and deletion of categories.

The automated CRUD test suite achieved five passing tests with no failures.

Overall, the testing demonstrated the current API's functional correctness and measured its response behaviour under the tested local conditions.

---

**END OF PERFORMANCE TESTING REPORT**