
const API_URL = "http://127.0.0.1:8000";

const token = localStorage.getItem("access_token");
let currentUsername = null;

if (!token) {
    window.location.href = "index.html";
}

const headers = {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json"
};

// CATEGORY DATABASE MAPPING
let categoryMap = {};

async function loadCategories() {
    try {
        const response = await fetch(`${API_URL}/api/categories`);

        if (!response.ok) {
            throw new Error("Unable to load categories.");
        }

        const categories = await response.json();

        categories.forEach(category => {
            categoryMap[category.category_name.toLowerCase()] =
                category.category_id;
        });

        console.log("Categories loaded:", categoryMap);

    } catch (error) {
        console.error("Category loading error:", error);
        selectionMessage.textContent =
            "Unable to load categories. Please refresh the page.";
    }
}

// LOAD USER PROFILE
async function loadProfile() {
    try {
        const response = await fetch(`${API_URL}/api/users/me`, {
            method: "GET",
            headers: headers
        });

        if (response.status === 401) {
            logout();
            return;
        }

        if (!response.ok) {
            throw new Error("Unable to load profile.");
        }

        const user = await response.json();

        currentUsername = user.username;

        document.getElementById("username").textContent =
            user.username;

    } catch (error) {
        console.error("Profile error:", error);
    }
}

// LOAD QUIZ STATISTICS
async function loadStatistics() {
    try {
        const response = await fetch(
            `${API_URL}/api/quizzes/history`,
            {
                method: "GET",
                headers: headers
            }
        );

        if (response.status === 401) {
            logout();
            return;
        }

        if (!response.ok) {
            throw new Error("Unable to load quiz history.");
        }

        const attempts = await response.json();

        const completedAttempts = attempts.filter(
            attempt => attempt.status === "completed"
        );

        const quizzesPlayed = completedAttempts.length;

        const totalScore = completedAttempts.reduce(
            (sum, attempt) => sum + attempt.score,
            0
        );

        const totalQuestions = completedAttempts.reduce(
            (sum, attempt) => sum + attempt.total_questions,
            0
        );

        const correctAnswers = completedAttempts.reduce(
            (sum, attempt) => sum + attempt.correct_answers,
            0
        );

        const accuracy = totalQuestions > 0
            ? Math.round((correctAnswers / totalQuestions) * 100)
            : 0;

        document.getElementById("quizzesPlayed").textContent =
            quizzesPlayed;

        document.getElementById("totalScore").textContent =
            totalScore;

        document.getElementById("accuracy").textContent =
            `${accuracy}%`;

    } catch (error) {
        console.error("Statistics error:", error);
    }
}

// CATEGORY AND DIFFICULTY SELECTION
let selectedCategory = null;
let selectedCategoryId = null;
let selectedDifficulty = null;

const categoryCards = document.querySelectorAll(".category-card");
const difficultyButtons = document.querySelectorAll(".difficulty-btn");

const selectionMessage =
    document.getElementById("selectionMessage");

const startQuizBtn =
    document.getElementById("startQuizBtn");

// UPDATE SELECTION
function updateSelection() {
    if (selectedCategory && selectedDifficulty) {
        selectionMessage.textContent =
            `${selectedCategory} | ${selectedDifficulty} difficulty selected.`;

        startQuizBtn.disabled = false;
    } else {
        selectionMessage.textContent =
            "Choose a category and difficulty to begin.";

        startQuizBtn.disabled = true;
    }
}

// SELECT CATEGORY
categoryCards.forEach(card => {
    card.addEventListener("click", () => {

        selectedCategory = card.dataset.category;

        selectedCategoryId =
            categoryMap[selectedCategory.toLowerCase()];

        categoryCards.forEach(item => {
            item.style.borderColor = "";
        });

        card.style.borderColor = "#c16aff";

        if (!selectedCategoryId) {
            selectionMessage.textContent =
                "This category is not available in the database yet.";

            startQuizBtn.disabled = true;
            return;
        }

        updateSelection();
    });
});

// EXPLORE BUTTONS
document.querySelectorAll(".category-btn").forEach(button => {
    button.addEventListener("click", () => {

        const card = button.closest(".category-card");

        if (card) {
            card.click();
        }

        document.querySelector(".difficulty-section")
            .scrollIntoView({ behavior: "smooth" });
    });
});

// SELECT DIFFICULTY
difficultyButtons.forEach(button => {
    button.addEventListener("click", () => {

        selectedDifficulty = button.dataset.difficulty;

        difficultyButtons.forEach(item => {
            item.classList.remove("selected");
        });

        button.classList.add("selected");

        updateSelection();
    });
});

// START QUIZ USING FASTAPI
startQuizBtn.addEventListener("click", async () => {

    if (!selectedCategoryId || !selectedDifficulty) {
        return;
    }

    startQuizBtn.disabled = true;
    startQuizBtn.textContent = "Loading Quiz...";

    selectionMessage.textContent =
        "Preparing your quiz. Please wait...";

    try {
        const response = await fetch(
            `${API_URL}/api/quizzes/start`,
            {
                method: "POST",
                headers: headers,
                body: JSON.stringify({
                    category_id: selectedCategoryId,
                    difficulty: selectedDifficulty,
                    total_questions: 4
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to start quiz."
            );
        }

        sessionStorage.setItem(
            "quizData",
            JSON.stringify(data)
        );

        window.location.href = "quiz.html";

    } catch (error) {
        selectionMessage.textContent = error.message;
        selectionMessage.style.color = "#ff7777";

        console.error("Quiz start error:", error);

        startQuizBtn.disabled = false;
        startQuizBtn.textContent = "Start Quiz";
    }
});

// LOAD LEADERBOARD
async function loadLeaderboard() {

    const leaderboardBtn =
        document.getElementById("leaderboardBtn");

    const leaderboardSection =
        document.getElementById("leaderboard");

    if (!leaderboardBtn || !leaderboardSection) {
        console.error("Leaderboard HTML elements not found.");
        return;
    }

    let resultsContainer =
        document.getElementById("leaderboardResults");

    if (!resultsContainer) {
        resultsContainer = document.createElement("div");
        resultsContainer.id = "leaderboardResults";
        leaderboardSection.appendChild(resultsContainer);
    }

    leaderboardBtn.disabled = true;
    leaderboardBtn.textContent = "Loading...";

    resultsContainer.textContent = "Loading leaderboard...";

    try {
        const response = await fetch(
            `${API_URL}/api/leaderboard/`
        );

        if (!response.ok) {
            throw new Error("Unable to load leaderboard.");
        }

        const players = await response.json();

        resultsContainer.replaceChildren();

        if (players.length === 0) {
            resultsContainer.textContent =
                "No completed quizzes yet. Be the first to play!";
            return;
        }

        const heading = document.createElement("h3");
        heading.textContent = "Top Players";
        resultsContainer.appendChild(heading);

        const table = document.createElement("table");
        table.className = "leaderboard-table";

        const headersList = [
            "Rank",
            "Player",
            "Total Score",
            "Quizzes Played",
            "Accuracy"
        ];

        const thead = document.createElement("thead");
        const headerRow = document.createElement("tr");

        headersList.forEach(title => {
            const th = document.createElement("th");
            th.textContent = title;
            headerRow.appendChild(th);
        });

        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement("tbody");

        players.forEach(player => {

            const row = document.createElement("tr");

            const isCurrentUser =
                currentUsername &&
                player.username.toLowerCase() ===
                currentUsername.toLowerCase();

            if (isCurrentUser) {
                row.classList.add("current-user-row");
            }

            if (player.rank === 1) {
                row.classList.add("leaderboard-first");
            }

            const values = [
                `#${player.rank}`,
                isCurrentUser
                    ? `${player.username} (You)`
                    : player.username,
                player.total_score,
                player.quizzes_played,
                `${player.accuracy}%`
            ];

            values.forEach(value => {
                const td = document.createElement("td");
                td.textContent = value;
                row.appendChild(td);
            });

            tbody.appendChild(row);
        });

        table.appendChild(tbody);
        resultsContainer.appendChild(table);

    } catch (error) {
        resultsContainer.textContent = error.message;
        console.error("Leaderboard error:", error);

    } finally {
        leaderboardBtn.disabled = false;
        leaderboardBtn.textContent = "View Leaderboard";
    }
}

// LEADERBOARD BUTTON
const leaderboardBtn =
    document.getElementById("leaderboardBtn");

if (leaderboardBtn) {
    leaderboardBtn.addEventListener("click", loadLeaderboard);
}

// LOGOUT
function logout() {
    localStorage.removeItem("access_token");
    sessionStorage.clear();
    window.location.href = "index.html";
}

document.getElementById("logoutBtn").addEventListener(
    "click",
    logout
);

// LOAD DASHBOARD DATA
loadCategories();
loadProfile();
loadStatistics();

