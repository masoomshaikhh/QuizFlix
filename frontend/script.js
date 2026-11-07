
// Get the login form and message area
const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");

// Handle login
loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    message.textContent = "Logging in...";
    message.style.color = "white";

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/auth/login",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );

        const data = await response.json();

        if (response.ok) {
            // Save the JWT token
            localStorage.setItem("access_token", data.access_token);

            message.textContent = "Login successful!";
            message.style.color = "#00ff88";

            // Redirect to dashboard after successful login
            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 700);

        } else {
            message.textContent = data.detail || "Login failed.";
            message.style.color = "#ff4444";
        }

    } catch (error) {
        message.textContent = "Unable to connect to the server.";
        message.style.color = "#ff4444";

        console.error("Login error:", error);
    }
});
