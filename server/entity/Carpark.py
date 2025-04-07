from server.DatabaseCtrl.DBFactory import DBFactory
from typing import List, Dict

class Carpark:
    """
    A class representing a Carpark with attributes for storing information regarding carpark.

    :param carpark_id: Unique identifier for the carpark.
    :type carpark_id: str

    :param address: Address of the carpark.
    :type address: str

    :param X_coord: X-coordinate of the carpark.
    :type X_coord: float

    :param Y_coord: Y-coordinate of the carpark.
    :type Y_coord: float

    :param carpark_type: Type of the carpark.
    :type carpark_type: str

    :param parking_system: Type of parking system used at the carpark.
    :type parking_system: str

    :param short_term_parking: Timing for short-term parking.
    :type short_term_parking: str

    :param free_parking: Timing for free parking.
    :type free_parking: str

    :param night_parking: True if night parking is available, False otherwise.
    :type night_parking: bool

    :param carpark_decks: Number of decks in the carpark.
    :type carpark_decks: int

    :param gantry_height: Height of the gantry system.
    :type gantry_height: float

    :param carpark_basement: True if the carpark has a basement, False otherwise.
    :type carpark_basement: bool
    """

    def __init__(self, carpark_id: str = '', address: str = '', X_coord: float = 0.00, 
                 Y_coord: float = 0.00, carpark_type: str = '', parking_system: str = '',
                 short_term_parking: str = '', free_parking: str = '', night_parking: bool = False, 
                 carpark_decks: int = 0, gantry_height: float = 0.00, 
                 carpark_basement: bool = False) -> None:
        """
        Initializes a carpark instance with the provided details.
        """
        self.carpark_id = carpark_id
        self.address = address
        self.X_coord = X_coord
        self.Y_coord = Y_coord
        self.carpark_type = carpark_type
        self.parking_system = parking_system
        self.short_term_parking = short_term_parking
        self.free_parking = free_parking
        self.night_parking = night_parking
        self.carpark_decks = carpark_decks
        self.gantry_height = gantry_height
        self.carpark_basement = carpark_basement
        self.carparkQueries = DBFactory().create_db_connection("Carpark")

    def new_carpark_from_db(self, exclude_ids: List[int]) -> "Carpark":
        """
        Fetches a new carpark from the database that is not in the provided list of excluded IDs.

        :param exclude_ids: List of carpark IDs to exclude.
        :type exclude_ids: List[int]
        
        :return: A Carpark instance with data from the DB or a fallback Carpark if none found.
        :rtype: Carpark
        """
        try:
            data = self.carparkQueries.fetch_one_carpark(exclude_ids)

            if data:
                self.carpark_id = data.get('carpark_id')
                self.address = data.get('address')
                self.X_coord = data.get('X_coord')
                self.Y_coord = data.get('Y_coord')
                self.carpark_type = data.get('carpark_type')
                self.parking_system = data.get('parking_system')
                self.short_term_parking = data.get('short_term_parking')
                self.free_parking = data.get('free_parking')
                self.night_parking = data.get('night_parking')
                self.carpark_decks = data.get('carpark_decks')
                self.gantry_height = data.get('gantry_height')
                self.carpark_basement = data.get('carpark_basement')
            else:
                # Return a fallback Carpark if no data is found
                return Carpark()

            return self
        except Exception as e:
            print(f"Error fetching carpark from DB: {e}")
            return Carpark()

    def insert_into_database(self) -> None:
        """
        Inserts the current carpark instance into the database.
        """
        try:
            print("Inserting carpark into the database...")

            self.carparkQueries.insert_carpark(
                carpark_id=self.carpark_id,
                address=self.address,
                X_coord=self.X_coord,
                Y_coord=self.Y_coord,
                carpark_type=self.carpark_type,
                parking_system=self.parking_system,
                short_term_parking=self.short_term_parking,
                free_parking=self.free_parking,
                night_parking=self.night_parking,
                carpark_decks=self.carpark_decks,
                gantry_height=self.gantry_height,
                carpark_basement=self.carpark_basement
            )
            print("Carpark inserted successfully.")
        except Exception as e:
            print(f"Error inserting carpark into DB: {e}")

    def get_full_history(self, user_id: int) -> Dict[int, Dict[str, str]]:
        """
        Retrieves the full carpark history for a specific user.

        :param user_id: The user ID for which the history is fetched.
        :type user_id: int

        :return: A dictionary of carpark history entries indexed by history number.
        :rtype: Dict[int, Dict[str, str]]
        """
        try:
            full_history = self.carparkQueries.fetch_all_history(user_id)
            history = {index: data for index, data in enumerate(full_history, start=1)}
            return history
        except Exception as e:
            print(f"Error fetching carpark history: {e}")
            return {}
        
    def get_all_carparks(self):
        """
        Fetches all carpark data from the database.

        :return: A list of dictionaries representing all carparks.
        :rtype: List[Dict[str, str]]
        """
        try:
            return self.carparkQueries.fetch_all_carparks()
        except Exception as e:
            print(f"Error fetching all carpark data: {e}")
            return {}