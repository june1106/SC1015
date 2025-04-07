document.getElementById('showPassword').addEventListener('change', function () {
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('re-enter-password');
    if (this.checked) {
        passwordField.type = 'text';  // Show password
        confirmPasswordField.type = 'text';  // Show confirm password
    } else {
        passwordField.type = 'password';  // Hide password
        confirmPasswordField.type = 'password';  // Hide confirm password
    }
});

function validatePassword(password) {
    const passwordPattern = /^(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,16}$/;
    return passwordPattern.test(password);
}

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

async function register() {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('re-enter-password').value;

    if (username === "" || !username || !email || !password || !confirmPassword) {
        alert('Please fill in the blank fields.');
        return;
    }

    if (!validateEmail(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    if (!validatePassword(password)) {
        alert('Your password must contain 8 to 16 characters, at least 1 uppercase character, and at least 1 special character.');
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    const registrationData = {
        username: username,
        email: email,
        password: password
    };

    await registerDataInServer(registrationData);
}

async function registerDataInServer(data) {
    console.log("Data being sent:", data); // Added for debugging

    fetch('http://127.0.0.1:5000/register', { // Confirmed correct API endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Ensured correct Content-Type
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errData => {
                    throw new Error(errData.error || response.statusText);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            alert('Registration successful.');

            sessionStorage.setItem('userID', data.userID);
            window.location.href = 'http://127.0.0.1:5000/login'; // Corrected URL for redirection
        })
        .catch(error => {
            alert(error.message === "Registration failed. Username or email already exists."
                ? "Registration failed. Username or email already exists."
                : "An error occurred. Please try again.");
        });
}
