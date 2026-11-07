
const resultData = JSON.parse(
    sessionStorage.getItem("quizResult") || "null"
);

// ==========================================
// CHECK WHETHER QUIZ RESULTS EXIST
// ==========================================

if (!resultData) {
    alert("No quiz results found. Please play a quiz first.");
    window.location.href = "dashboard.html";
}

// ==========================================
// DISPLAY QUIZ RESULTS
// ==========================================

if (resultData) {

    document.getElementById("finalScore").textContent =
        resultData.score;

    document.getElementById("correctAnswers").textContent =
        resultData.correct_answers;

    document.getElementById("totalQuestions").textContent =
        resultData.total_questions;

    document.getElementById("finalAccuracy").textContent =
        `${resultData.accuracy}%`;

    const accuracy = resultData.accuracy;
    let message = "";

    if (accuracy === 100) {
        message = "Perfect Score! You're an Entertainment Expert! 🏆";
    } else if (accuracy >= 75) {
        message = "Excellent Work! Keep it up! 🌟";
    } else if (accuracy >= 50) {
        message = "Good Job! You're getting there! 🎯";
    } else {
        message = "Keep Practising! You'll do better next time! 💜";
    }

    document.getElementById("resultMessage").textContent = message;
}

// ==========================================
// ANSWER REVIEW SECTION
// ==========================================

function displayAnswerReview() {

    const resultCard = document.querySelector(".result-card");

    const dashboardBtn =
        document.getElementById("dashboardBtn");

    if (!resultCard) {
        console.error("Result card not found.");
        return;
    }

    // Create the answer review section
    const reviewSection = document.createElement("section");

    reviewSection.id = "answerReview";
    reviewSection.className = "answer-review-section";

    const heading = document.createElement("h2");
    heading.textContent = "Answer Review 📝";

    const description = document.createElement("p");
    description.textContent =
        "Review your answers and learn from your mistakes.";

    reviewSection.appendChild(heading);
    reviewSection.appendChild(description);

    const reviews = Array.isArray(resultData.review)
        ? resultData.review
        : [];

    // Handle missing review data
    if (reviews.length === 0) {

        const emptyMessage = document.createElement("p");

        emptyMessage.textContent =
            "Answer review is unavailable for this attempt.";

        reviewSection.appendChild(emptyMessage);

    } else {

        reviews.forEach((item, index) => {

            const isCorrect = item.is_correct;

            // Individual question card
            const questionCard = document.createElement("div");

            questionCard.className =
                isCorrect
                    ? "answer-review-card correct-answer"
                    : "answer-review-card incorrect-answer";

            // Question heading
            const questionHeading = document.createElement("h3");

            questionHeading.textContent =
                `Question ${index + 1}`;

            // Correct / Incorrect status
            const status = document.createElement("span");

            status.className = "answer-review-status";

            status.textContent = isCorrect
                ? "✓ Correct"
                : "✗ Incorrect";

            // Actual question
            const questionText = document.createElement("p");

            questionText.className = "review-question";

            questionText.textContent = item.question_text;

            // Player's selected answer
            const selectedAnswer = document.createElement("p");

            selectedAnswer.className = "review-selected-answer";

            selectedAnswer.textContent =
                `Your answer: ${item.selected_option_text}`;

            // Correct answer
            const correctAnswer = document.createElement("p");

            correctAnswer.className = "review-correct-answer";

            correctAnswer.textContent =
                `Correct answer: ${item.correct_option_text}`;

            // Explanation
            const explanation = document.createElement("p");

            explanation.className = "review-explanation";

            explanation.textContent =
                `Explanation: ${item.explanation || "No explanation available."}`;

            // Add elements to question card
            questionCard.appendChild(questionHeading);
            questionCard.appendChild(status);
            questionCard.appendChild(questionText);
            questionCard.appendChild(selectedAnswer);

            if (!isCorrect) {
                questionCard.appendChild(correctAnswer);
            }

            questionCard.appendChild(explanation);

            reviewSection.appendChild(questionCard);
        });
    }

    // Insert answer review before dashboard button
    if (dashboardBtn && dashboardBtn.parentNode === resultCard) {

        resultCard.insertBefore(
            reviewSection,
            dashboardBtn
        );

    } else {

        resultCard.appendChild(reviewSection);
    }
}

// Display answer review after quiz submission
if (resultData) {
    displayAnswerReview();
}

// ==========================================
// RETURN TO DASHBOARD
// ==========================================

const dashboardBtn =
    document.getElementById("dashboardBtn");

if (dashboardBtn) {

    dashboardBtn.addEventListener("click", () => {

        sessionStorage.removeItem("quizData");
        sessionStorage.removeItem("quizResult");

        window.location.href = "dashboard.html";
    });
}

// ==========================================
// LOGOUT
// ==========================================

const logoutBtn =
    document.getElementById("logoutBtn");

if (logoutBtn) {

    logoutBtn.addEventListener("click", () => {

        localStorage.removeItem("access_token");
        sessionStorage.clear();

        window.location.href = "index.html";
    });
}

