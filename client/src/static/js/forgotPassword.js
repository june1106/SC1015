document.getElementById('showPassword').addEventListener('change', function () {
    const passwordField = document.getElementById('new-password');
    if (this.checked) {
        passwordField.type = 'text';  // Show password
    } else {
        passwordField.type = 'password';  // Hide password
    }
});

function validatePassword(password) {
    const passwordPattern = /^(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,16}$/;
    return passwordPattern.test(password);
}

async function resetPassword(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('new-password').value;

    if (!validatePassword(password)) {
        alert('Your password must contain at least 8 characters, at least 1 uppercase character, and at least 1 special character.');
        return;
    }

    const response = await fetch('http://127.0.0.1:5000/forgotPassword', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            username: username,
            password: password
        })
    });

    const result = await response.json();

    if (response.ok) {
        if (response.status === 201) {
            alert('Password reset successfully!');
            window.location.href = '/'
        }
    }
    else if (response.status === 401) {
        // Login failed, show error message
        alert('Reset failed: ' + result.error);
    }
    else {
        // Handle other errors
        alert('An error occurred: ' + result.error);
    }
}