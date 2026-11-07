
# ==========================================================
# QUIZFLIX - PERFORMANCE AND API TESTING
# Lab 8: Software Engineering Assignment
# Libraries: Requests, Pandas, NumPy
# ==========================================================

import time
import requests
import pandas as pd
import numpy as np

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


# ----------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------

BASE_URL = "http://127.0.0.1:8000"

ENDPOINTS = [
    "/health",
    "/api/leaderboard/"
]

TOTAL_REQUESTS = 100
MAX_WORKERS = 10

OUTPUT_DIR = Path(__file__).resolve().parent

results = []


# ----------------------------------------------------------
# FUNCTION: SEND ONE REQUEST
# ----------------------------------------------------------

def send_request(url):

    start_time = time.perf_counter()

    try:
        response = requests.get(
            url,
            timeout=15
        )

        elapsed = (
            time.perf_counter() - start_time
        ) * 1000

        try:
            response.json()
            valid_json = True
        except ValueError:
            valid_json = False

        return {
            "status_code": response.status_code,
            "response_time_ms": elapsed,
            "success": response.ok and valid_json,
            "valid_json": valid_json,
            "error": ""
        }

    except requests.RequestException as error:

        elapsed = (
            time.perf_counter() - start_time
        ) * 1000

        return {
            "status_code": None,
            "response_time_ms": elapsed,
            "success": False,
            "valid_json": False,
            "error": str(error)
        }


# ----------------------------------------------------------
# FUNCTION: RUN SEQUENTIAL TEST
# ----------------------------------------------------------

def sequential_test(endpoint):

    url = BASE_URL + endpoint

    measurements = []

    print(f"\nSequential test: {endpoint}")

    start_time = time.perf_counter()

    for number in range(TOTAL_REQUESTS):

        result = send_request(url)

        measurements.append(result)

    total_time = time.perf_counter() - start_time

    return calculate_metrics(
        endpoint,
        "Sequential",
        measurements,
        total_time
    )


# ----------------------------------------------------------
# FUNCTION: RUN CONCURRENT TEST
# ----------------------------------------------------------

def concurrent_test(endpoint):

    url = BASE_URL + endpoint

    measurements = []

    print(f"\nConcurrent test: {endpoint}")

    start_time = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures = [
            executor.submit(send_request, url)
            for _ in range(TOTAL_REQUESTS)
        ]

        for future in as_completed(futures):

            measurements.append(future.result())

    total_time = time.perf_counter() - start_time

    return calculate_metrics(
        endpoint,
        "Concurrent",
        measurements,
        total_time
    )


# ----------------------------------------------------------
# FUNCTION: CALCULATE PERFORMANCE METRICS
# ----------------------------------------------------------

def calculate_metrics(
    endpoint,
    test_type,
    measurements,
    total_time
):

    response_times = np.array([
        item["response_time_ms"]
        for item in measurements
    ])

    successful = sum(
        1 for item in measurements
        if item["success"]
    )

    failed = len(measurements) - successful

    error_rate = (
        failed / len(measurements)
    ) * 100

    throughput = (
        len(measurements) / total_time
        if total_time > 0
        else 0
    )

    metrics = {
        "endpoint": endpoint,
        "test_type": test_type,
        "requests": len(measurements),
        "successful": successful,
        "failed": failed,
        "error_rate_percent": round(error_rate, 2),
        "minimum_ms": round(np.min(response_times), 2),
        "maximum_ms": round(np.max(response_times), 2),
        "average_ms": round(np.mean(response_times), 2),
        "median_ms": round(np.median(response_times), 2),
        "p95_ms": round(np.percentile(response_times, 95), 2),
        "throughput_rps": round(throughput, 2),
        "total_time_seconds": round(total_time, 2)
    }

    results.append(metrics)

    print("\nPerformance Results:")
    print("--------------------------------")

    for key, value in metrics.items():
        print(f"{key}: {value}")

    return metrics


# ----------------------------------------------------------
# HTTP METHOD TESTING
# ----------------------------------------------------------

def test_http_methods():

    print("\n========== HTTP METHOD TESTING ==========")

    url = BASE_URL + "/health"

    methods = [
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    ]

    method_results = []

    for method in methods:

        start_time = time.perf_counter()

        try:

            response = requests.request(
                method,
                url,
                json={},
                timeout=15
            )

            elapsed = (
                time.perf_counter() - start_time
            ) * 1000

            try:
                response.json()
                valid_json = True
            except ValueError:
                valid_json = False

            record = {
                "method": method,
                "status_code": response.status_code,
                "response_time_ms": round(elapsed, 2),
                "valid_json": valid_json
            }

        except requests.RequestException as error:

            record = {
                "method": method,
                "status_code": None,
                "response_time_ms": None,
                "valid_json": False
            }

            print("Request error:", error)

        method_results.append(record)

        print(record)

    method_df = pd.DataFrame(method_results)

    method_df.to_csv(
        OUTPUT_DIR / "http_method_results.csv",
        index=False
    )

    return method_df


# ----------------------------------------------------------
# MAIN EXECUTION
# ----------------------------------------------------------

if __name__ == "__main__":

    print("\n========== QUIZFLIX PERFORMANCE TESTING ==========")

    print("Total requests per test:", TOTAL_REQUESTS)
    print("Concurrent workers:", MAX_WORKERS)

    # Check server availability first.
    try:
        health = requests.get(
            BASE_URL + "/health",
            timeout=5
        )

        health.raise_for_status()

    except requests.RequestException as error:

        print("\nBackend is unavailable:", error)
        print("Start the FastAPI server and run again.")
        raise SystemExit(1)

    # Run tests against each read-only endpoint.
    for endpoint in ENDPOINTS:

        sequential_test(endpoint)

        concurrent_test(endpoint)

    # Test HTTP method restrictions.
    method_df = test_http_methods()

    # Save performance report.
    performance_df = pd.DataFrame(results)

    performance_df.to_csv(
        OUTPUT_DIR / "performance_results.csv",
        index=False
    )

    print("\n========== FINAL PERFORMANCE SUMMARY ==========")

    print(performance_df.to_string(index=False))

    print("\n========== HTTP METHOD SUMMARY ==========")

    print(method_df.to_string(index=False))

    print("\nGenerated files:")
    print("performance_results.csv")
    print("http_method_results.csv")

    print("\n========== TESTING COMPLETED ==========\n")
