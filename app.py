from server.controllers.CarparkCtrl import CarparkCtrl
from server.controllers.DestinationCtrl import DestinationCtrl
from server.controllers.UserCtrl import UserCtrl
from server.DatabaseCtrl.UserQueries import UserQueries
from server.entity.User import User
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import logging
from rapidfuzz.fuzz import ratio
import ast

import requests

app = Flask(__name__, 
            template_folder='client/src/pages',
            static_folder='client/src/static')
app.url_map.strict_slashes = False
app.secret_key = 'your_secret_key'  # Added for session management

CORS(app)

user_queries = UserQueries()
user = User()
user_ctrl = UserCtrl(user)
carpark_ctrl = CarparkCtrl()

def get_token():
    """
    Retrieves an access token from the OneMap API.

    This function sends a POST request to the OneMap API's token endpoint with the
    required email and password credentials. If the request is successful, it extracts
    and returns the access token from the response. Otherwise, it prints an error message.

    Returns:
        str: The access token if the request is successful, None otherwise.
    """
    url = "https://www.onemap.gov.sg/api/auth/post/getToken"
    data = {
        "email": "ngziyunalol@gmail.com",  # Replace with your email
        "password": "Lol1234567890!"       # Replace with your password
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        return access_token
    else:
        print("Error:", response.status_code, response.text)
        return None
    
def get_carpark_distance(start_coords, end_coords, access_token):
    temp_url_p1 = "https://www.onemap.gov.sg/api/public/routingsvc/route?"
    temp_url_p2 = "&routeType=drive"
    temp_url = f"{temp_url_p1}start={start_coords}&end={end_coords}{temp_url_p2}"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(temp_url, headers=headers).json()
        return response['route_summary']['total_distance']
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching carpark distance: {e}")
        return None

requested_ids = []

@app.route('/', methods=['GET'])
def home():
    """
    Home route that checks if the user is logged in.
    Redirects to the destination input page if logged in, otherwise show the home page.

    Returns:
        Response: A rendered home page or a redirect.
    """

    global user
    if user is None:
        user = User()
    return render_template('index.html')

@app.route('/get_access_token', methods=['GET'])
def get_access_token():
    """
    Endpoint to retrieve the access token from the OneMap API.

    This route calls the `get_token` function to fetch the access token and returns it as a JSON response.

    Returns:
        Response: A JSON response containing the access token or an error message.
    """
    access_token = get_token()
    if access_token:
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Failed to retrieve access token."}), 500
    
@app.route('/register', methods=['GET'])
def show_register():
    '''
    Displays the registration page.
    
    This route renders the register.html template.
    Users visit this route to view the registration form.

    Returns:
        Response: The rendered HTMl template for the registration page.
    '''

    return render_template('register.html')

@app.route('/login', methods=['GET'])
def show_login():
    '''
    Display the login page.
    This route renders the 'login.html' template.
    Users visit this route to view the login form.
    
    Returns:
        Response: The rendered HTML template for the login page.
    '''
    return render_template('login.html')

@app.route('/inputDestination', methods=['GET'])
def show_inputDestination():
    '''
    Display the destination input page.
    This route renders the inputDestination.html template.
    
    Returns:
        Response: The rendered HTML template for the destination input page.
    '''
    
    return render_template('inputDestination.html')

@app.route('/inputCarpark', methods=['GET'])
def show_inputCarpark():
    '''
    Display the carpark selection page.
    This route renders the inputCarpark.html template.
    Returns:
        Reponse: The rendered HTML template for the carpark selection page.
    '''

    return render_template('inputCarpark.html')

@app.route('/history', methods=['GET'])
def show_history():
    """
    Display the user's history page.
    This route renders the history.html template.

    Returns:
        Response: The rendered HTML template for the history page.
    """

    return render_template('history.html')

@app.route('/logout', methods=['GET'])
def logout():
    '''
    Log out the user.
    This route logs out the user by setting their 'logged_in' flag to False and
    clearing their User object. After logging out, the user is redirected to the
    home page.

    Returns:
        Response: A redirect to the home page after logging out.
    '''

    global user
    user.logged_in = False
    user = None
    return redirect(url_for('home'))

@app.route('/forgotPassword', methods=['GET'])
def show_forgotPassword():
    '''
    Display the reset password page.
    This route renders the resetPassword.html template.
    Returns:
        Reponse: The rendered HTML template for the forgot password page.
    '''

    return render_template('forgotPassword.html')

@app.route('/forgotPassword', methods=['POST'])
def forgotPassword():
    '''
    Handles reset password functionality.
    This route accepts JSON data for username, email and password, and attempts
    to reset the password for user. It checks if the username or email already exists. 
    If found, it returns a success response. Otherwise, it returns an error message.
    The `password` is updated in the database using the `update_user_password` method.
    
    Args:
        request.get_json(): JSON payload containing the username, email and password.
        
    Returns:
        Response: A JSON response indicating whether the reset was successful,
        including an appropriate status code.
    '''

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    result = user_queries.find_user_id(username, email, password)

    if result == 0:  # User does not exist
        return jsonify({"error": "Reset failed. Username or Email does not exist."}), 400

    if result != 0: # Successful reset
        global user
        user.update_all_attributes(user_id=result, username=username, email=email, password=password)
        temp = user_queries.update_user_password(username=username, email=email, new_password=password)
        if temp == True:
            return jsonify({"success": "Reset successful.", "userID": result}), 201
        else:
            return jsonify({"error": "Failed to reset password."}), 400
    return jsonify({"error": "Failed to reset password."}), 500


@app.route('/register', methods=['POST'])
def register():
    '''
    Register a new user.
    This route accepts JSON data for username, email and password, and attempts
    to register a new user. It checks if the username or email already exists
    and if not, inserts the new user into the database. If the registration is 
    successful, it returns a success response. Otherwise, it returns an error message.
    
    Args:
        request.get_json(): JSON payload containing the username, email and password.
        
    Returns:
        Response: A JSON response indicating whether the registration was successful,
        including an appropriate status code.
    '''

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if user_queries.does_username_or_email_exist(username, email):
        return jsonify({"error": "Registration failed. Username or email already exists."}), 400
    
    result = user_queries.insert_new_user(username, email, password)

    if result != 0: # Successful insertion
        global user
        user.update_all_attributes(user_id=result, username=username, email=email, password=password, logged_in=True)
        return jsonify({"success": "Registration successful.", "userID": result}), 201
    
    return jsonify({"error": "Failed to register user."}), 500

@app.route('/login', methods=['POST'])
def login():
    '''
    Handles the login functionality for a user. This route accepts a POST request with a JSON payload
    containing the username and password, verifies the user's credentials, and returns the appropriate
    response.

    Parameters:
        - username (str): The username of the user attempting to log in.
        - password (str): The password of the user attempting to log in.

    Returns:
        - JSON response:
            - If login is successful, returns the userID and a URL for redirection:
                {
                    "userID": userID,
                    "redirect_url": URL of the next page 
                }
            - If the username or password is incorrect, returns:
                {
                    "error": "Invalid username or password."
                }
            - If there is an internal server error, returns:
                {
                    "error": "An error occurred while processing your request."
                }

    Exceptions:
        - Handles general exceptions, logs the error, and returns a 500 Internal Server Error response
          with a generic error message.
    '''

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
        user_id = user_queries.find_user_id(username, "", password)

        if user_id:
            global user
            user.user_id = user_id
            user.login_user()
            session['logged_in'] = True  # Added for session management
            return jsonify({"user_id": user_id, "redirect_url": url_for('show_inputDestination')}), 200 # redirect to destination input
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        # Log the error (optional, depending on your logging setup) 
        print(f"Error during login: {str(e)}")
        return jsonify({"error": "An error occured while processing your request"}), 500 # Internal server error  

@app.route('/getCarparks', methods=['POST'])
def get_carparks():
    data = request.get_json()
    destination = data.get('destinationValue')
    destination = ast.literal_eval(destination)
    vehicle_type = data.get('vehicleSearch')
    if vehicle_type == "Car/Van":
        vehicle_type = "C"
    elif vehicle_type == "Motorcycle":
        vehicle_type = "M"
    elif vehicle_type == "Heavy":
        vehicle_type = "H"

    if not destination:
        return jsonify({"error": "No carparks found."}), 404

    # Extract destination address
    destination_address = destination.get('ADDRESS', '').lower()
    start_coords = f"{destination['LATITUDE']},{destination['LONGITUDE']}"
    lst = carpark_ctrl.get_carparks()  # Ensure this function is implemented

    access_token = get_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    # Set similarity threshold (adjustable)
    SIMILARITY_THRESHOLD = 40

    # Compute similarity scores and filter based on threshold
    url = "https://api.data.gov.sg/v1/transport/carpark-availability"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch carpark data."}), 500
    carpark_data = response.json()['items'][0]['carpark_data']

    # Filter carparks based on availability
    available_carparks = {
        carpark['carpark_number']: lot
        for carpark in carpark_data
        for lot in carpark['carpark_info'] if lot['lot_type'] == vehicle_type
    }
    
    # Compare with carparks from the database
    lst = [
    {
        **carpark,
        "lots_available": int(available_carparks[carpark['carpark_id']]['lots_available'])  # Add available lots
    }
        for carpark in lst
        if carpark['carpark_id'] in available_carparks and (available_carparks[carpark['carpark_id']]['lot_type'] == vehicle_type and int(available_carparks[carpark['carpark_id']]['lots_available']) > 0)
    ]

    filtered_lst = [
        carpark for carpark in lst
        if ratio(destination_address, carpark.get('address', '').lower()) >= SIMILARITY_THRESHOLD
    ]

    def fetch_carpark_distance(carpark):
        url_p1 = "https://www.onemap.gov.sg/api/public/revgeocodexy?"
        url_p2 = "&buffer=40&addressType=All&otherFeatures=N"
        url = f"{url_p1}location={carpark['X_coord']},{carpark['Y_coord']}{url_p2}"
        try:
            response = requests.get(url, headers=headers).json()
            end_coords = f"{response['GeocodeInfo'][0]['LATITUDE']},{response['GeocodeInfo'][0]['LONGITUDE']}"
            return get_carpark_distance(start_coords, end_coords, access_token)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching carpark data for {carpark}: {e}")
            return None

    with ThreadPoolExecutor() as executor:
        distances = list(executor.map(fetch_carpark_distance, filtered_lst))
    
    # Filter out any None results (failed requests)
    valid_distances = [(i, dist) for i, dist in enumerate(distances) if dist is not None]
    sorted_carpark_dist = dict(sorted(valid_distances, key=lambda x: x[1]))

    sorted_carpark_dist_list = list(sorted_carpark_dist.items())[:4]  # Convert to list before slicing
    result = [filtered_lst[key] for key, _ in sorted_carpark_dist_list]

    return jsonify({"result": result}), 200

@app.route('/getCurrentUser', methods=["POST"])
def get_current_user():
    '''
    Retrieves the currently logged-in user's username
    
    This route checks if the user is logged in and returns the username. If the user is
    not logged in, an error message is returned.
    
    Args:
        None: This route does not require any input parameters. It uses the global user
              object to determine the logged-in status and retrieves the username.
    
    Returns:
        JSON response:
            - On success: A JSON object containing the username of the currently loggeed-in user.
            - On failure: A JSON object with an error message if the user is not logged in.
    
    Raises:
        None: No exceptions are raised as the route relies on the global user object for logged-in status.
    '''

    if user.is_logged_in():
        tempUser = user_queries.get_user_by_id(user.user_id)
        user.update_all_attributes(user_id=tempUser.user_id, username=tempUser.username, email=tempUser.email, password=tempUser.password)
        return jsonify({"username": user.username}), 200
    else:
        return jsonify({"error": "User not logged in."}), 400

@app.route('/addDestinations', methods=['POST'])
def addDestinations():
    '''
    Adds a new destination for a user for a specific datetime.
    
    This route allows the user to add a new destination for a specific datetime.
    
    Args:
        request (JSON): The request body should contain the following keys:
            - 'carpark_id' : The ID of the carpark to add to the destination
            - 'datetime' : The datetime for which to add the destination
            
    Returns:
        JSON response:
            - On success: A JSON object containing a success message indicating that
              the destination was added successfully.
            - On failure: A JSON object containing an error message.
    
    Raises:
        Exception: Any exception that may occur during the adding process will
                   be captured and returned as an error response. 
    '''

    ctrl = DestinationCtrl()
    data = request.get_json()
    carpark_id = data.get('carpark_id')
    dt = datetime.now()
    if ctrl.create_destination(user.user_id, carpark_id, dt) is None:
        print("None")
        return jsonify({"error": "Destination was not added successfully."}), 409
    return jsonify({"message": "Destination added successfully."}), 201

@app.route('/loadHistory', methods=['POST'])
def loadHistory():
    '''
    Retrieves the history for a user.
    
    This route allows the user to fetch all the carparks previously parked at by the user
    from the database. It returns a list of carparks associated with the user's account.''
    
    Args:
        None: The function uses the current logged-in user's ID to fetch the history.
        
    Returns:
        JSON response:
            - On success: A JSON array containing the list of carparks from the user's history.
            - On failure: A JSON object containing an error message if no carparks are found.
    
    Raises:
        Exception: Any exception that might occur during the database
                  query will be captured and returned in the error response.
    '''
    
    ctrl = CarparkCtrl()
    alldestinations = ctrl.get_History(user.user_id)

    if alldestinations:
        return jsonify(alldestinations), 200
    elif not user.is_logged_in():
        return jsonify({"error": "You must log in to track your search history."}), 401 
    else:
        return jsonify({"error": "There are no past search history."}), 404

if __name__=="__main__":
    app.run(debug=True, port=5000)

