
// Get the registration form
const registerForm = document.getElementById("registerForm");

// Get the message area
const registerMessage = document.getElementById("registerMessage");

// Listen for registration submission
registerForm.addEventListener("submit", async function(event) {

    // Prevent page refresh
    event.preventDefault();

    // Get form values
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    // Check whether passwords match
    if (password !== confirmPassword) {
        registerMessage.textContent = "Passwords do not match!";
        registerMessage.style.color = "#ff6b8a";
        return;
    }

    // Show progress message
    registerMessage.textContent = "Creating your account...";
    registerMessage.style.color = "#d5aaff";

    try {

        // Send registration details to FastAPI
        const response = await fetch(
            "http://127.0.0.1:8000/api/auth/register",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            }
        );

        // Read server response
        const data = await response.json();

        if (response.ok) {

            registerMessage.textContent =
                "Account created successfully! You can now log in.";

            registerMessage.style.color = "#8dffbd";

            // Clear registration form
            registerForm.reset();

        } else {

            registerMessage.textContent =
                typeof data.detail === "string"
                    ? data.detail
                    : "Registration failed. Please check your details.";

            registerMessage.style.color = "#ff6b8a";
        }

    } catch (error) {

        registerMessage.textContent =
            "Unable to connect to the server.";

        registerMessage.style.color = "#ff6b8a";

        console.error("Registration error:", error);
    }

});
