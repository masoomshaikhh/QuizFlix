
# ==========================================================
# QUIZFLIX - DATA SCIENCE AND MACHINE LEARNING
# Lab 5: Data Science Framework
# Algorithm: Decision Tree Classifier
# Dataset: Simulated Quiz Performance Data
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    ConfusionMatrixDisplay
)


# ----------------------------------------------------------
# 1. INITIALIZATION
# ----------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "quizflix_ml_training_data.csv"

rng = np.random.default_rng(42)

print("\n========== QUIZFLIX DATA SCIENCE FRAMEWORK ==========\n")


# ----------------------------------------------------------
# 2. GENERATE SIMULATED DATASET
# ----------------------------------------------------------

print("Generating simulated QuizFlix training data...")

records = []

difficulty_settings = {
    "Easy": {
        "accuracy_min": 0.65,
        "accuracy_max": 0.98,
        "duration_mean": 75,
        "duration_std": 18
    },
    "Medium": {
        "accuracy_min": 0.40,
        "accuracy_max": 0.80,
        "duration_mean": 115,
        "duration_std": 22
    },
    "Hard": {
        "accuracy_min": 0.15,
        "accuracy_max": 0.65,
        "duration_mean": 155,
        "duration_std": 28
    }
}

for difficulty, settings in difficulty_settings.items():

    for i in range(120):

        total_questions = int(rng.integers(8, 13))

        accuracy_rate = rng.uniform(
            settings["accuracy_min"],
            settings["accuracy_max"]
        )

        correct_answers = int(
            round(accuracy_rate * total_questions)
        )

        duration = int(
            rng.normal(
                settings["duration_mean"],
                settings["duration_std"]
            )
        )

        duration = max(30, duration)

        actual_accuracy = (
            correct_answers / total_questions
        ) * 100

        records.append({
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "score": correct_answers * 10,
            "duration_seconds": duration,
            "accuracy": round(actual_accuracy, 2),
            "difficulty": difficulty
        })


df = pd.DataFrame(records)

df.to_csv(DATA_FILE, index=False)

print("Dataset generated successfully!")
print("Dataset shape:", df.shape)


# ----------------------------------------------------------
# 3. DATA INSPECTION
# ----------------------------------------------------------

print("\n========== DATASET PREVIEW ==========")

print(df.head())

print("\nDataset information:")

df.info()

print("\nStatistical summary:")

print(df.describe())


# ----------------------------------------------------------
# 4. DATA PREPROCESSING
# ----------------------------------------------------------

print("\n========== DATA PREPROCESSING ==========")

print("\nMissing values:")

print(df.isnull().sum())

print("\nDuplicate records:", df.duplicated().sum())

df = df.drop_duplicates()

print("Dataset after duplicate removal:", df.shape)


# ----------------------------------------------------------
# 5. EXPLORATORY DATA ANALYSIS (EDA)
# ----------------------------------------------------------

print("\n========== EXPLORATORY DATA ANALYSIS ==========")

difficulty_summary = df.groupby("difficulty").agg(
    average_score=("score", "mean"),
    average_accuracy=("accuracy", "mean"),
    average_duration=("duration_seconds", "mean"),
    total_attempts=("difficulty", "count")
).round(2)

print(difficulty_summary)


# ----------------------------------------------------------
# 6. DATA VISUALIZATION
# ----------------------------------------------------------

plt.figure(figsize=(8, 5))

df["difficulty"].value_counts().reindex(
    ["Easy", "Medium", "Hard"]
).plot(kind="bar")

plt.title("QuizFlix - Difficulty Distribution")
plt.xlabel("Difficulty")
plt.ylabel("Number of Attempts")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    BASE_DIR / "ml_difficulty_distribution.png",
    dpi=300
)

plt.close()


# ----------------------------------------------------------
# 7. FEATURE SELECTION
# ----------------------------------------------------------

features = [
    "total_questions",
    "correct_answers",
    "duration_seconds",
    "accuracy"
]

X = df[features]

y = df["difficulty"]

print("\nSelected Features:")

print(features)

print("\nTarget Variable: difficulty")


# ----------------------------------------------------------
# 8. TRAIN-TEST SPLIT
# ----------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print("\n========== TRAIN-TEST SPLIT ==========")

print("Training records:", len(X_train))

print("Testing records:", len(X_test))


# ----------------------------------------------------------
# 9. BUILD MACHINE LEARNING MODEL
# ----------------------------------------------------------

print("\n========== MODEL TRAINING ==========")

model = DecisionTreeClassifier(
    max_depth=4,
    min_samples_leaf=4,
    random_state=42
)

model.fit(X_train, y_train)

print("Decision Tree model trained successfully!")


# ----------------------------------------------------------
# 10. MAKE PREDICTIONS
# ----------------------------------------------------------

predictions = model.predict(X_test)

print("\n========== MODEL PREDICTIONS ==========")

print("Actual values:")

print(y_test.to_numpy()[:10])

print("\nPredicted values:")

print(predictions[:10])


# ----------------------------------------------------------
# 11. EVALUATE MODEL
# ----------------------------------------------------------

accuracy = accuracy_score(y_test, predictions)

print("\n========== MODEL EVALUATION ==========")

print("Model Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# ----------------------------------------------------------
# 12. CONFUSION MATRIX
# ----------------------------------------------------------

ConfusionMatrixDisplay.from_predictions(
    y_test,
    predictions
)

plt.title("QuizFlix - Model Confusion Matrix")
plt.tight_layout()

plt.savefig(
    BASE_DIR / "ml_confusion_matrix.png",
    dpi=300
)

plt.close()


# ----------------------------------------------------------
# 13. FEATURE IMPORTANCE
# ----------------------------------------------------------

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values(
    by="Importance",
    ascending=False
)

print("\n========== FEATURE IMPORTANCE ==========")

print(importance)

plt.figure(figsize=(8, 5))

plt.bar(
    importance["Feature"],
    importance["Importance"]
)

plt.title("QuizFlix - Feature Importance")
plt.xlabel("Features")
plt.ylabel("Importance Score")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    BASE_DIR / "ml_feature_importance.png",
    dpi=300
)

plt.close()


# ----------------------------------------------------------
# 14. FINAL SUMMARY
# ----------------------------------------------------------

print("\n========== FINAL SUMMARY ==========")

print("Total simulated records:", len(df))

print("Algorithm: Decision Tree Classifier")

print("Training records:", len(X_train))

print("Testing records:", len(X_test))

print("Model accuracy:", round(accuracy * 100, 2), "%")

print("\nGenerated output files:")

print(DATA_FILE.name)
print("ml_difficulty_distribution.png")
print("ml_confusion_matrix.png")
print("ml_feature_importance.png")

print("\n========== DATA SCIENCE ANALYSIS COMPLETED ==========\n")
