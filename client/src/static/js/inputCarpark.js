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

    let userID = sessionStorage.getItem('userID');
    if (!userID) {
        userID = 0;
        sessionStorage.setItem('userID', userID);
    }
    console.log(userID)

    async function getUsername() {
        const userID = sessionStorage.getItem('userID');
        console.log(userID)

        fetch('http://127.0.0.1:5000/getCurrentUser', {
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

    const carparkGrid = document.getElementById('carpark-grid');
    let currentCarparkCount = 0;
    let carparkShown = [];
    let filteredCarpark = [];

    // Load carpark data from sessionStorage
    async function loadcarpark() {
        let data = JSON.parse(sessionStorage.getItem("carparkData")) || {}; // Retrieve stored carpark data
        console.log("Loaded data from sessionStorage:", data);

        // Iterate over the data object and add it to the array
        Object.values(data.result).forEach((carpark, index) => {
            console.log(typeof carpark)
            carparkShown[currentCarparkCount + index + 1] = carpark;
        });

        currentCarparkCount += Object.values(data).length;
        filteredCarpark = carparkShown;

        console.log("Current carpark count:", currentCarparkCount);
        updateCarparkGrid();
    }

    // Create a card element for each carpark
    function createcarparkCard(carpark) {
        if (!carpark) {
            console.error("Received invalid carpark object", carpark);
            return;
        }

        const availableLots = carpark.lots_available || 0;
        const availabilityClass = availableLots > 5 ? 'good-availability' :
            availableLots > 0 ? 'low-availability' : 'no-availability';

        console.log("Creating card for carpark:", carpark);  // Debugging the carpark object

        const card = document.createElement('div');
        card.className = 'carpark-card';

        // Ensure you are accessing the object properties correctly
        card.innerHTML = `
            <div class="carpark-info" style="display: flex; flex-direction: row; justify-content: space-between; align-items: center; padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 10px; background-color: #f9f9f9;">
            <div style="flex: 1; text-align: left;">
            <h3 style="margin: 0;">${carpark.carpark_id || 'N/A'}</h3>
            <p style="margin: 5px 0;">${carpark.address || 'No Address Available'}</p>
            <p style="margin: 5px 0; color: ${availableLots > 0 ? '#2ecc71' : '#e74c3c'}">
                    Available Lots: ${availableLots}
            </p>
            </div>
            <div style="flex: 2; display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-between;">
            <p style="margin: 0;">X: ${carpark.X_coord || 'Not Available'}</p>
            <p style="margin: 0;">Y: ${carpark.Y_coord || 'Not Available'}</p>
            <p style="margin: 0;">Type: ${carpark.carpark_type || 'Not Available'}</p>
            <p style="margin: 0;">System: ${carpark.parking_system || 'Not Available'}</p>
            <p style="margin: 0;">Short Term: ${carpark.short_term_parking || 'Not Available'}</p>
            <p style="margin: 0;">Free Parking: ${carpark.free_parking || 'Not Available'}</p>
            <p style="margin: 0;">Night Parking: ${carpark.night_parking === 1 ? 'Yes' : carpark.night_parking === 0 ? 'No' : 'Not Available'}</p>
            <p style="margin: 0;">Decks: ${carpark.carpark_decks || 'Not Available'}</p>
            <p style="margin: 0;">Gantry Height: ${carpark.gantry_height || 'Not Available'}</p>
            <p style="margin: 0;">Basement: ${carpark.carpark_basement || 'Not Available'}</p>
            </div>
            </div>
        `;
        return card;
    }

    // Initialize the map
    let sw = L.latLng(1.144, 103.535);
    let ne = L.latLng(1.494, 104.502);
    let bounds = L.latLngBounds(sw, ne);

    let map = L.map('map', {
        center: L.latLng(1.2868108, 103.8545349),
        zoom: 16
    });

    map.setMaxBounds(bounds);

    let basemap = L.tileLayer('https://www.onemap.gov.sg/maps/tiles/Original/{z}/{x}/{y}.png', {
        detectRetina: true,
        maxZoom: 19,
        minZoom: 11,
        /** DO NOT REMOVE the OneMap attribution below **/
        attribution: '<img src="https://www.onemap.gov.sg/web-assets/images/logo/om_logo.png" style="height:20px;width:20px;"/>&nbsp;<a href="https://www.onemap.gov.sg/" target="_blank" rel="noopener noreferrer">OneMap</a>&nbsp;&copy;&nbsp;contributors&nbsp;&#124;&nbsp;<a href="https://www.sla.gov.sg/" target="_blank" rel="noopener noreferrer">Singapore Land Authority</a>'
    });

    basemap.addTo(map);

    // Add markers for carparks and destination
    function addMarkersToMap() {
        if (!filteredCarpark || filteredCarpark.length === 0) {
            console.log("No carparks to map.");
            return;
        }

        async function getAccessToken() {
            try {
                const response = await fetch('http://127.0.0.1:5000/get_access_token', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch access token: ' + response.status);
                }
                const data = await response.json();
                return data.access_token;
            } catch (error) {
                console.error('Error fetching access token:', error);
                return null;
            }
        }

        async function convertCoordsToLatLng(x, y) {
            try {
                const accessToken = await getAccessToken();
                if (!accessToken) {
                    console.error('Access token is required to proceed.');
                    return null;
                }
                const response = await fetch(`https://www.onemap.gov.sg/api/public/revgeocodexy?location=${x},${y}&buffer=40&addressType=All&otherFeatures=N`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `${accessToken}`,
                    }
                });
                if (!response.ok) {
                    throw new Error('Failed to convert coordinates: ' + response.status);
                }
                const data = await response.json();
                return { lat: data.GeocodeInfo[0].LATITUDE, lng: data.GeocodeInfo[0].LONGITUDE };
            } catch (error) {
                console.error('Error converting coordinates:', error);
                return null;
            }
        }

        async function addDestination(destination) {
            try {
                const response = await fetch('http://127.0.0.1:5000/addDestinations', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(destination)
                });
                if (!response.ok) {
                    throw new Error('Failed to add destination: ' + response.status);
                }
                const data = await response.json();
                console.log("Destination stored on server:", data);
            } catch (error) {
                console.error('Error adding destination:', error);
            }
        }

        let routingControl = null;
        let userMarker = null;

        for (const carpark of filteredCarpark) {
            if (carpark && carpark.X_coord && carpark.Y_coord) {
                convertCoordsToLatLng(carpark.X_coord, carpark.Y_coord).then(latLng => {
                    if (latLng) {
                        const marker = L.marker([latLng.lat, latLng.lng]).addTo(map);
                        const popupContent = document.createElement('div');
                        popupContent.innerHTML = `
                    <b>${carpark.carpark_id || 'N/A'}</b><br>
                    ${carpark.address || 'No Address Available'}<br>
                    Type: ${carpark.carpark_type || 'Not Available'}
                `;

                        const routeButton = document.createElement('button');
                        routeButton.textContent = 'Show Route';
                        routeButton.style.marginTop = '10px';

                        routeButton.addEventListener('click', () => {
                            if (navigator.geolocation) {
                                navigator.geolocation.getCurrentPosition(position => {
                                    const userLat = position.coords.latitude;
                                    const userLng = position.coords.longitude;

                                    if (userMarker) {
                                        map.removeLayer(userMarker);
                                    }

                                    userMarker = L.marker([userLat, userLng], { draggable: true }).addTo(map)
                                        .bindPopup("You are here").openPopup();

                                    if (routingControl) {
                                        map.removeControl(routingControl);
                                    }

                                    routingControl = L.Routing.control({
                                        waypoints: [
                                            L.latLng(userLat, userLng),
                                            L.latLng(latLng.lat, latLng.lng)
                                        ],
                                        plan: L.Routing.plan([
                                            L.latLng(userLat, userLng),
                                            L.latLng(latLng.lat, latLng.lng)
                                        ], {
                                            draggableWaypoints: false,
                                            addWaypoints: false
                                        }),
                                        routeWhileDragging: true
                                    }).addTo(map);

                                    const routingContainer = document.querySelector('.leaflet-routing-container');
                                    if (routingContainer) {
                                        routingContainer.style.backgroundColor = 'white';
                                        routingContainer.style.opacity = '1';
                                    }

                                    console.log(`Routing from (${userLat}, ${userLng}) to (${latLng.lat}, ${latLng.lng})`);

                                    const destinationData = { user_id: userID, lat: latLng.lat, lng: latLng.lng, carpark_id: carpark.carpark_id };
                                    addDestination(destinationData);
                                }, error => {
                                    console.error('Error getting user location:', error);
                                });
                            } else {
                                console.error('Geolocation is not supported by this browser.');
                            }
                        });

                        popupContent.appendChild(routeButton);
                        marker.bindPopup(popupContent);
                        marker.on('click', () => {
                            console.log(`Clicked on carpark: ${carpark.carpark_id}`);
                        });
                    }
                }).catch(error => {
                    console.error('Error resolving latLng:', error);
                });
            }
        }
    }

    const destination = { lat: 1.3521, lng: 103.8198 }; // Default coordinates for Singapore
    let destinationdata = JSON.parse(sessionStorage.getItem("destination")) || {};
    destination.lat = destinationdata.LATITUDE;
    destination.lng = destinationdata.LONGITUDE;
    map.setView([destination.lat, destination.lng], 16);
    console.log('Destination coordinates updated:', destination);
    const destinationMarker = L.marker([destination.lat, destination.lng], {
        icon: L.icon({
            iconUrl: '../static/img/destination.png', iconSize: [25, 41], iconAnchor: [12, 41]
        })
    }).addTo(map);
    destinationMarker.bindPopup('<b>Destination</b>');
    destinationMarker.on('click', () => {
        console.log('Clicked on destination');
    });

    // Update the carpark grid
    function updateCarparkGrid() {
        carparkGrid.innerHTML = '';  // Clear the grid

        if (!filteredCarpark || filteredCarpark.length === 0) {
            alert("No carparks found.");
            nocarparkMessage.style.display = 'block';
        } else {
            nocarparkMessage.style.display = 'none';
            console.log(typeof filteredCarpark);
            console.log(filteredCarpark.length);
            filteredCarpark.forEach((carpark) => {
                const card = createcarparkCard(carpark);
                carparkGrid.appendChild(card);
                console.log('Carpark appended:', carpark);
            });
        }
    }

    const nocarparkMessage = document.createElement('p');
    nocarparkMessage.className = 'no-carpark-message';
    nocarparkMessage.textContent = 'There are no carparks.';
    carparkGrid.appendChild(nocarparkMessage);

    getUsername();  // Fetch the username
    // Call the function to add markers after loading carparks
    loadcarpark().then(() => {
        addMarkersToMap();
    });
});
