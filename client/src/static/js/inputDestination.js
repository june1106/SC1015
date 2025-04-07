// Function to search for carparks based on the destination input
async function searchCarparks(event) {
    event.preventDefault();

    const destination = document.getElementById('destinationValue').value;
    const vehicle = document.getElementById('vehicleSearch').value;

    // ❗ Show message if destination is empty
    if (!destination || destination.trim() === "") {
        alert('Destination cannot be empty. Please input a destination.');
        return;
    }

    const response = await fetch('http://127.0.0.1:5000/getCarparks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            vehicleSearch: vehicle,
            destinationValue: destination
        })
    });

    const result = await response.json();

    if (response.ok) {
        if (response.status === 200) {
            alert('Search successful!');
            sessionStorage.setItem('carparkData', JSON.stringify(result));
            sessionStorage.setItem('destination', destination);
            sessionStorage.setItem('vehicle', JSON.stringify(vehicle));
            window.location.href = '/inputCarpark';
        }
    } else {
        alert('Search failed: ' + (result.error || 'An error occurred.'));
    }
}


async function autocompleteDestination() {
    const input = document.getElementById('destinationSearch').value;
    const suggestionsBox = document.getElementById('destinationSuggestions');
    suggestionsBox.innerHTML = ''; // Clear previous suggestions

    if (input.length < 3) return; // Wait until the user types at least 3 characters

    try {
        const response = await fetch(`https://www.onemap.gov.sg/api/common/elastic/search?searchVal=+${input}+&returnGeom=Y&getAddrDetails=Y`)
        if (!response.ok) throw new Error('Failed to fetch suggestions');
        const result = await response.json();
        let suggestions = result.results || [];
        suggestions.forEach(destination => {
            const suggestionDiv = document.createElement('div');
            suggestionDiv.textContent = `${destination.SEARCHVAL}, ${destination.BLK_NO}, ${destination.ROAD_NAME}, ${destination.BUILDING}, ${destination.ADDRESS}, ${destination.POSTAL}`;
            suggestionDiv.onclick = () => selectDestination(destination);
            suggestionsBox.appendChild(suggestionDiv);
        });
    } catch (error) {
        console.error('Error fetching destination suggestions:', error);
    }
}

function selectDestination(destination) {
    document.getElementById('destinationValue').value = JSON.stringify(destination);
    document.getElementById('destinationSearch').value = `${destination.SEARCHVAL}, ${destination.BLK_NO}, ${destination.ROAD_NAME}, ${destination.BUILDING}, ${destination.ADDRESS}, ${destination.POSTAL}`;
    document.getElementById('destinationSuggestions').innerHTML = '';
}

document.addEventListener('DOMContentLoaded', function () {
    // Function to get the username
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
        console.log("UserID:", userID);

        fetch('http://127.0.0.1:5000/getCurrentUser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ userID: userID || "" })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch data: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                document.getElementById('username').innerText = data.username;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    // Function to select a vehicle and enable Step 2
    window.selectVehicle = function (vehicle) {
        document.getElementById("vehicleSearch").value = vehicle;
        document.getElementById("vehicleSuggestions").style.display = "none";

        // Enable Step 2
        document.getElementById("step2").classList.remove("disabled");
        document.getElementById("destinationSearch").disabled = false;
        document.getElementById("findParking").classList.add("active");
        document.getElementById("findParking").disabled = false;
    }

    // Show the suggestion box when clicking the input field (only set this once)
    document.getElementById("vehicleSearch").addEventListener("focus", function () {
        document.getElementById("vehicleSuggestions").style.display = "block";
    });

    // Always keep Find Parking button active once vehicle is selected
document.getElementById("destinationSearch").addEventListener("input", function () {
    let findParkingBtn = document.getElementById("findParking");
    findParkingBtn.classList.add("active");
    findParkingBtn.disabled = false;
});


    // Call the function to get username
    getUsername();
});
