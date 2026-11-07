
# ==========================================================
# QUIZFLIX - DATA HANDLING AND ANALYSIS
# Lab 4: Software Engineering Assignment
# Libraries: Pandas, NumPy, Matplotlib
# Dataset: Simulated Quiz Attempt Data
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ----------------------------------------------------------
# 1. LOAD DATASET
# ----------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "quizflix_analytics.csv"

OUTPUT_FILE = BASE_DIR / "cleaned_quizflix_analytics.csv"

print("\n========== QUIZFLIX DATA ANALYSIS ==========\n")

df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")

print("Dataset loaded successfully!")
print("Original dataset shape:", df.shape)


# ----------------------------------------------------------
# 2. INSPECT DATASET
# ----------------------------------------------------------

print("\n========== DATASET PREVIEW ==========")

print(df.head())

print("\n========== DATASET INFORMATION ==========")

df.info()

print("\n========== STATISTICAL SUMMARY ==========")

print(df.describe(include="all"))


# ----------------------------------------------------------
# 3. IDENTIFY MISSING VALUES
# ----------------------------------------------------------

print("\n========== MISSING VALUES ==========")

print(df.isnull().sum())

print("\nTotal missing values:", df.isnull().sum().sum())


# ----------------------------------------------------------
# 4. IDENTIFY AND REMOVE DUPLICATES
# ----------------------------------------------------------

print("\n========== DUPLICATE RECORDS ==========")

duplicate_count = df.duplicated().sum()

print("Duplicate records found:", duplicate_count)

df = df.drop_duplicates()

print("Dataset shape after removing duplicates:", df.shape)


# ----------------------------------------------------------
# 5. HANDLE MISSING VALUES
# ----------------------------------------------------------

print("\n========== HANDLING MISSING VALUES ==========")

# Fill missing category values.
df["category"] = df["category"].fillna("Unknown")

# Convert numeric columns to numeric data types.
numeric_columns = [
    "total_questions",
    "correct_answers",
    "score",
    "duration_seconds"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Replace missing duration with median duration.
median_duration = df["duration_seconds"].median()

df["duration_seconds"] = df["duration_seconds"].fillna(
    median_duration
)

print("Missing category values replaced with 'Unknown'.")
print("Missing duration values replaced with median:", median_duration)


# ----------------------------------------------------------
# 6. CREATE ACCURACY COLUMN USING NUMPY
# ----------------------------------------------------------

df["accuracy"] = np.where(
    df["total_questions"] > 0,
    (df["correct_answers"] / df["total_questions"]) * 100,
    0
)

df["accuracy"] = df["accuracy"].round(2)

print("\n========== ACCURACY CALCULATION ==========")

print(
    df[["player_id", "correct_answers", "total_questions", "accuracy"]]
)


# ----------------------------------------------------------
# 7. FILTER DATA
# ----------------------------------------------------------

print("\n========== FILTERING DATA ==========")

high_scoring_players = df[df["score"] >= 40]

print("Players scoring 40 or above:")

print(high_scoring_players)


# ----------------------------------------------------------
# 8. SORT DATA
# ----------------------------------------------------------

print("\n========== SORTING DATA ==========")

sorted_data = df.sort_values(
    by="score",
    ascending=False
)

print("Players sorted by score (highest first):")

print(
    sorted_data[
        ["player_id", "category", "score", "accuracy"]
    ]
)


# ----------------------------------------------------------
# 9. GROUP DATA BY CATEGORY
# ----------------------------------------------------------

print("\n========== CATEGORY-WISE ANALYSIS ==========")

category_analysis = df.groupby("category").agg(
    total_attempts=("attempt_id", "count"),
    average_score=("score", "mean"),
    average_accuracy=("accuracy", "mean"),
    average_duration=("duration_seconds", "mean")
).round(2)

print(category_analysis)


# ----------------------------------------------------------
# 10. GROUP DATA BY DIFFICULTY
# ----------------------------------------------------------

print("\n========== DIFFICULTY-WISE ANALYSIS ==========")

difficulty_analysis = df.groupby("difficulty").agg(
    attempts=("attempt_id", "count"),
    average_score=("score", "mean"),
    average_accuracy=("accuracy", "mean")
).round(2)

print(difficulty_analysis)


# ----------------------------------------------------------
# 11. NUMPY STATISTICAL OPERATIONS
# ----------------------------------------------------------

print("\n========== NUMPY ANALYSIS ==========")

scores = df["score"].to_numpy()

print("All scores:", scores)

print("Average score:", np.mean(scores))

print("Median score:", np.median(scores))

print("Maximum score:", np.max(scores))

print("Minimum score:", np.min(scores))

print("Score standard deviation:", round(np.std(scores), 2))

print("75th percentile:", np.percentile(scores, 75))


# ----------------------------------------------------------
# 12. SAVE CLEANED DATASET
# ----------------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned dataset saved successfully:")
print(OUTPUT_FILE)


# ----------------------------------------------------------
# 13. VISUALIZATION 1: CATEGORY-WISE AVERAGE SCORE
# ----------------------------------------------------------

plt.figure(figsize=(9, 5))

category_analysis["average_score"].plot(
    kind="bar"
)

plt.title("QuizFlix - Average Score by Category")
plt.xlabel("Entertainment Category")
plt.ylabel("Average Score")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

plt.savefig(
    BASE_DIR / "category_performance.png",
    dpi=300
)

plt.close()


# ----------------------------------------------------------
# 14. VISUALIZATION 2: SCORE DISTRIBUTION
# ----------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.hist(
    scores,
    bins=6,
    edgecolor="black"
)

plt.title("QuizFlix - Score Distribution")
plt.xlabel("Quiz Score")
plt.ylabel("Number of Attempts")
plt.tight_layout()

plt.savefig(
    BASE_DIR / "score_distribution.png",
    dpi=300
)

plt.close()


# ----------------------------------------------------------
# 15. VISUALIZATION 3: DIFFICULTY-WISE AVERAGE ACCURACY
# ----------------------------------------------------------

plt.figure(figsize=(8, 5))

difficulty_analysis["average_accuracy"].plot(
    kind="bar"
)

plt.title("QuizFlix - Average Accuracy by Difficulty")
plt.xlabel("Difficulty Level")
plt.ylabel("Average Accuracy (%)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    BASE_DIR / "difficulty_analysis.png",
    dpi=300
)

plt.close()


# ----------------------------------------------------------
# 16. FINAL SUMMARY
# ----------------------------------------------------------

print("\n========== FINAL ANALYSIS SUMMARY ==========")

print("Original records:", 22)

print("Duplicate records removed:", duplicate_count)

print("Final cleaned records:", len(df))

print("Average quiz score:", round(df["score"].mean(), 2))

print("Average quiz accuracy:", round(df["accuracy"].mean(), 2))

print("\nThree visualizations generated successfully!")

print("\n========== ANALYSIS COMPLETED ==========\n")
