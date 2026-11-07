
const API_URL = "http://127.0.0.1:8000";

const token = localStorage.getItem("access_token");
const quizData = JSON.parse(sessionStorage.getItem("quizData") || "null");

let currentQuestionIndex = 0;
let selectedAnswers = {};

// Check authentication and quiz data
if (!token) {
    window.location.href = "index.html";
}

if (!quizData || !quizData.questions || quizData.questions.length === 0) {
    alert("No active quiz found. Please start a new quiz.");
    window.location.href = "dashboard.html";
}

// Load quiz information
function loadQuiz() {
    if (!quizData) return;

    document.getElementById("quizCategory").textContent =
        "QuizFlix Entertainment Challenge";

    document.getElementById("quizDifficulty").textContent =
        `${quizData.difficulty} Difficulty`;

    showQuestion();
}

// Display current question
function showQuestion() {
    const questions = quizData.questions;
    const question = questions[currentQuestionIndex];

    document.getElementById("questionProgress").textContent =
        `Question ${currentQuestionIndex + 1} of ${questions.length}`;

    document.getElementById("questionText").textContent =
        question.question_text;

    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

    document.getElementById("progressBar").style.width =
        `${progress}%`;

    const optionsContainer =
        document.getElementById("optionsContainer");

    optionsContainer.innerHTML = "";

    const nextButton = document.getElementById("nextQuestionBtn");
    const submitButton = document.getElementById("submitQuizBtn");

    const isLastQuestion =
        currentQuestionIndex === questions.length - 1;

    question.options.forEach(option => {
        const button = document.createElement("button");

        button.className = "quiz-option";
        button.textContent = option.option_text;

        if (selectedAnswers[question.question_id] === option.option_id) {
            button.classList.add("selected");
        }

        button.addEventListener("click", () => {

            selectedAnswers[question.question_id] = option.option_id;

            document.querySelectorAll(".quiz-option").forEach(item => {
                item.classList.remove("selected");
            });

            button.classList.add("selected");

            if (isLastQuestion) {
                submitButton.disabled = false;
            } else {
                nextButton.disabled = false;
            }
        });

        optionsContainer.appendChild(button);
    });

    // Configure navigation buttons
    nextButton.hidden = isLastQuestion;
    submitButton.hidden = !isLastQuestion;

    nextButton.disabled =
        !selectedAnswers[question.question_id];

    submitButton.disabled =
        !selectedAnswers[question.question_id];

    document.getElementById("quizMessage").textContent = "";
}

// Next question
document.getElementById("nextQuestionBtn").addEventListener("click", () => {

    if (currentQuestionIndex < quizData.questions.length - 1) {

        currentQuestionIndex++;

        showQuestion();
    }
});

// Submit quiz
document.getElementById("submitQuizBtn").addEventListener(
    "click",
    submitQuiz
);

async function submitQuiz() {

    const submitButton =
        document.getElementById("submitQuizBtn");

    const message =
        document.getElementById("quizMessage");

    const answers = quizData.questions.map(question => ({
        question_id: question.question_id,
        selected_option_id: selectedAnswers[question.question_id]
    }));

    if (answers.some(answer => !answer.selected_option_id)) {

        message.textContent =
            "Please answer every question before submitting.";

        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";

    try {

        const response = await fetch(
            `${API_URL}/api/quizzes/${quizData.attempt_id}/submit`,
            {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ answers })
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Quiz submission failed."
            );
        }

        sessionStorage.setItem(
            "quizResult",
            JSON.stringify(result)
        );

        window.location.href = "result.html";

    } catch (error) {

        message.textContent = error.message;
        message.style.color = "#ff7777";

        submitButton.disabled = false;
        submitButton.textContent = "Submit Quiz";

        console.error("Submission error:", error);
    }
}

// Quit quiz
document.getElementById("quitQuizBtn").addEventListener("click", () => {

    const confirmQuit = confirm(
        "Are you sure you want to quit this quiz?"
    );

    if (confirmQuit) {

        sessionStorage.removeItem("quizData");

        window.location.href = "dashboard.html";
    }
});

// Start displaying questions
if (quizData && quizData.questions && quizData.questions.length > 0) {
    loadQuiz();
}
