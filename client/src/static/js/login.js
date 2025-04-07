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

async function login(event) {
    event.preventDefault();  // Prevent the default form submission behavior

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Make the fetch call and store the response
    const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password,
        })
    });

    const result = await response.json();  // Parse the JSON from the response

    if (response.ok) {
        alert('Login successful.')
        sessionStorage.setItem('userID', result.user_id);
        console.log("UserID:", result.user_id);
        window.location.href = '/inputDestination';
    }
    else if (response.status === 401) {
        // Login failed, show error message
        alert('Login failed: ' + result.error);
    }
    else {
        // Handle other errors
        alert('An error occurred: ' + result.error);
    }
}