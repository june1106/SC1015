document.addEventListener('DOMContentLoaded', function () {
    async function logOut() {
        try {
            // Remove userID from session storage
            sessionStorage.removeItem('userID');

            // Send logout request to the server
            const response = await fetch('http://127.0.0.1:5000/logout', {
                method: 'GET'
            });

            // Check if the response is OK
            if (!response.ok) {
                throw new Error('Failed to logout: ' + response.status);
            }

            alert('Logout successful');
            window.location.href = '/';
        } catch (error) {
            console.error('Error logging out:', error);
        }
    }

    const logOutButton = document.getElementById('log-out-button');
    if (logOutButton) {
        logOutButton.addEventListener('click', logOut);
    } else {
        console.error("Element with ID 'log-out-button' not found in the DOM.");
    }

    async function getUsername() {
        const userID = sessionStorage.getItem('userID');
        console.log(userID)

        fetch('http://127.0.0.1:5000/getCurrentUser', {  // Your API URL here
            method: 'POST',  // Use POST to avoid showing parameters in URL
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ userID })  // Sending userID in the request body
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch data: ' + response.status);
                }
                return response.json();  // Parse JSON data
            })
            .then(data => {
                console.log(data);  // For debugging purposes
                document.getElementById('username').innerText = data.username; // Call the function to display the data
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    };

    const historyGrid = document.getElementById('history-grid');
    if (!historyGrid) {
        console.error("Element with ID 'history-grid' not found in the DOM.");
        return;
    }
    let currentHistoryCount = 0;
    let historyShown = [];
    let filteredHistory = [];

    async function loadHistory() {
        fetch('http://127.0.0.1:5000/loadHistory', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                number_of_history: 10
            })
        })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 401) {
                        throw new Error('Unauthorized access. Please log in.');
                    } else if (response.status === 404) {
                        throw new Error('History not found.');
                    } else if (response.status === 500) {
                        throw new Error('Server error. Please try again later.');
                    } else {
                        throw new Error('Failed to fetch data: ' + response.status);
                    }
                }
                return response.json();
            })
            .then(data => {
                console.log(data);

                Object.values(data).forEach((history, index) => {
                    historyShown[currentHistoryCount + index + 1] = history;
                });

                currentHistoryCount += Object.values(data).length;
                filteredHistory = historyShown;

                console.log(currentHistoryCount);
                updateHistoryGrid();
            })
            .catch(error => {
                console.error('Error fetching data:', error.message);
                if (error.message.includes('Unauthorized')) {
                    alert('You must be logged in to view your history.');
                } else if (error.message.includes('History not found')) {
                    noHistoryMessage.textContent = 'No past search history.';
                    noHistoryMessage.style.display = 'block';
                } else if (error.message.includes('Server error')) {
                    alert('There was an issue with the server. Please try again later.');
                } else {
                    alert('An unexpected error occurred. Please try again.');
                }
            });
    }

    function formatDateToLong(dateString) {
        const date = new Date(dateString);
        const day = date.getDate();
        const month = date.toLocaleString('default', { month: 'long' });
        const year = date.getFullYear();
        const hours = date.getHours();
        const minutes = date.getMinutes();
        return `${day} ${month} ${year} ${hours}:${minutes}`;
    }

    function createHistoryCard(destination) {
        const card = document.createElement('div');
        card.className = 'history-card';
        card.innerHTML = `
            <div class="history-info">
                <h3>${destination.carparkID}</h3>
                <p>${destination.address}</p>
                <p>${formatDateToLong(destination.datetime)}</p>
            </div>
        `;
        return card;
    }

    function updateHistoryGrid() {
        historyGrid.innerHTML = '';

        if (filteredHistory.length === 0) {
            console.log('empty');
            noHistoryMessage.style.display = 'block';
        } else {
            noHistoryMessage.style.display = 'none';
            filteredHistory.forEach((history) => {
                const card = createHistoryCard(history);
                historyGrid.appendChild(card);
                console.log('appended');
            });
        }
    }

    const noHistoryMessage = document.createElement('p');
    noHistoryMessage.className = 'no-history-message';
    const userID = sessionStorage.getItem('userID');
    if (!userID === 0) {
        noHistoryMessage.textContent = 'No past search history.';
    }
    else {
        noHistoryMessage.textContent = 'You must be logged in to view history.';
    }
    historyGrid.appendChild(noHistoryMessage);

    getUsername();
    loadHistory();
});