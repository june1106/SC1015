import requests
from server.entity.Carpark import Carpark

class CarparkCtrl:
    """
    Controller class for managing carpark-related operations.
    """
    def _fetch_carpark_data(self) -> dict:
        """
        Internal helper to fetch carpark data from data.gov.sg API.

        :return: JSON data if successful, empty dictionary otherwise.
        :rtype: dict
        """
        api_url = "https://data.gov.sg/api/action/datastore_search?resource_id=d_23f946fa557947f93a8043bbef41dd09&limit=5000"
        response = requests.get(api_url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching carparks: {response.status_code}")
            return {}

    def HDB_GetFullCarparkInfo_Count(self) -> list[dict]:
        """
        Fetch and store full carpark info from API into database.

        :return: List of parsed carpark information.
        :rtype: list[dict]: 
        """
        result = self._fetch_carpark_data().get('result', {})
        all_carparks = result.get('records')
        parsed_carparks = []

        for carpark in all_carparks:
            carpark_id = carpark.get('car_park_no')
            address = carpark.get('address')
            X_coord = float(carpark.get('x_coord', 0))
            Y_coord = float(carpark.get('y_coord', 0))
            carpark_type = carpark.get('car_park_type')
            parking_system = carpark.get('type_of_parking_system')
            free_parking = carpark.get('free_parking', '')
            night_parking = carpark.get('night_parking') == 'YES'
            carpark_decks = int(carpark.get('car_park_decks', 0))
            gantry_height = float(carpark.get('gantry_height', 0))
            carpark_basement = carpark.get('car_park_basement') == 'Y'

            carpark_data = {
                'carpark_id': carpark_id,
                'address': address,
                'X_coord': X_coord,
                'Y_coord': Y_coord,
                'carpark_type': carpark_type,
                'parking_system': parking_system,
                'free_parking': free_parking,
                'night_parking': night_parking,
                'carpark_decks': carpark_decks,
                'gantry_height': gantry_height,
                'carpark_basement': carpark_basement
            }

            carpark_obj = Carpark(**carpark_data)
            carpark_obj.insert_into_database()

            parsed_carparks.append(carpark_data)

        return parsed_carparks

    def get_History(self, user_id: int) -> list[dict]:
        """
        Retrieve full carpark history for a user.

        :param user_id: User's ID.
        :type user_id: int

        :return: List of carpark history entries.
        :rtype: list[dict]
        """
        return Carpark().get_full_history(user_id)

    def get_carpark(self, carpark_id: str) -> dict:
        """
        Fetch details for a specific carpark by carpark_id.

        :param carpark_id: The carpark ID.
        :type carpark_id: str

        :return: Carpark details if found, empty dict otherwise.
        :rtype: dict
        """
        try:
            result = self._fetch_carpark_data().get('result', {})
            all_carparks = result.get('records', [])
            found = next((c for c in all_carparks if c['car_park_no'] == carpark_id), None)
            return found or {}

        except requests.exceptions.RequestException as req_err:
            print(f"Request error: {req_err}")
            raise

        except Exception as err:
            print(f"Unexpected error: {err}")
            raise

    def get_carparks(self) -> list[dict]:
        """
        Fetch all carpark details from database.

        :return: List of carpark details.
        :rtype: list[dict]
        """
        try:
            result = Carpark().get_all_carparks()
            return result

        except requests.exceptions.RequestException as req_err:
            print(f"Request error: {req_err}")
            raise

        except Exception as err:
            print(f"Unexpected error: {err}")
            raise