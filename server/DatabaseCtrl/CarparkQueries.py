import sqlite3
from server.DatabaseCtrl.DatabaseQueries import DatabaseQueries

class CarparkQueries(DatabaseQueries):
    def __init__(self):
        super().__init__()

    def fetch_all_carparks(self) -> list[dict]:
        """
        Retrieves all carpark records from the database.

        :return: A list of dictionaries where each dictionary contains details of a carpark, including ID, address, coordinates, type, parking system, availability, and other attributes.
        :rtype: list[dict]
        """
        query = """
        SELECT * FROM Carparks;
        """
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            return [
                {
                    "carpark_id": row[0],
                    "address": row[1],
                    "X_coord": row[2],
                    "Y_coord": row[3],
                    "carpark_type": row[4],
                    "parking_system": row[5],
                    "short_term_parking": row[6],
                    "free_parking": row[7],
                    "night_parking": row[8],
                    "carpark_decks": row[9],
                    "gantry_height": row[10],
                    "carpark_basement": row[11],
                }
                for row in results
            ]
        except Exception as e:
            print("Error occurred while fetching all carpark data:", e)
            return []

    def fetch_one_carpark(self, exclude_list: list[int] = None) -> dict:
        """
        Retrieves a single random carpark from the database, excluding carparks 
        with IDs provided in the exclude list.

        :param exclude_list: A list of carpark IDs to exclude from the query. Defaults to an empty list.
        :type exclude_list: list[int], optional
        :return: A dictionary containing carpark details, or an empty dictionary if no matching carpark is found.
        :rtype: dict
        """
        if exclude_list is None:
            exclude_list = []

        placeholders = ', '.join(['?'] * len(exclude_list)) if exclude_list else 'NULL'
        query = f"""
        SELECT c.carpark_id, c.address, c.X_coord, c.Y_coord, c.carpark_type, c.parking_system,
        c.short_term_parking, c.free_parking, c.night_parking, c.carpark_decks, c.gantry_height,
        c.carpark_basement
        FROM Carparks c
        WHERE c.carpark_id NOT IN ({placeholders})
        ORDER BY RANDOM() LIMIT 1;
        """

        self.cursor.execute(query, exclude_list)
        carpark_row = self.cursor.fetchone()

        return {
            'carpark_id': carpark_row[0],
            'address': carpark_row[1],
            'X_coord': carpark_row[2],
            'Y_coord': carpark_row[3],
            'carpark_type': carpark_row[4], 
            'parking_system': carpark_row[5],
            'short_term_parking': carpark_row[6],
            'free_parking': carpark_row[7],
            'night_parking': carpark_row[8],
            'carpark_decks': carpark_row[9],
            'gantry_height': carpark_row[10],
            'carpark_basement': carpark_row[11]
        } if carpark_row else {}

    def insert_carpark(self, carpark_id: str = '', address: str = '', X_coord: float = 0.00, 
                 Y_coord: float = 0.00, carpark_type: str = '', parking_system: str = '',
                 short_term_parking: str = '', free_parking: str = '', night_parking: bool = False, 
                 carpark_decks: int = 0, gantry_height: float = 0.00, 
                 carpark_basement: bool = False) -> None:
        """
        Inserts a new carpark record into the database.

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

        :param parking_system: Type of parking system used.
        :type parking_system: str

        :param short_term_parking: Information about short-term parking.
        :type short_term_parking: str

        :param free_parking: Information about free parking availability.
        :type free_parking: str

        :param night_parking: Whether night parking is available.
        :type night_parking: bool

        :param carpark_decks: Number of decks in the carpark.
        :type carpark_decks: int

        :param gantry_height: Height of the gantry.
        :type gantry_height: float

        :param carpark_basement: Whether the carpark has a basement.
        :type carpark_basement: bool

        :return: None
        :rtype: None
    """
        
        query = """
        INSERT INTO carparks (carpark_id, address, X_coord, Y_coord, carpark_type, parking_system,
        short_term_parking, free_parking, night_parking, carpark_decks, gantry_height, 
        carpark_basement)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        values = (carpark_id, address, X_coord, Y_coord, carpark_type, parking_system, short_term_parking,
                  free_parking, night_parking, carpark_decks, gantry_height, carpark_basement)

        self.cursor.execute(query, values)
        self.connection.commit()
        print("Carpark inserted successfully")

    def fetch_all_history(self, user_id: int) -> list[dict]:
        """
        Retrieves the history of carparks visited by a specific user.

        :param user_id: The ID of the user whose carpark visit history is to be retrieved.
        :type user_id: int

        :return: A list of dictionaries with carpark ID, address, and visit timestamp.
        :rtype: list of dict
    """
        query = """
        SELECT 
            c.carpark_id, 
            c.address, 
            d.datetime
        FROM Destinations d
        INNER JOIN Carparks c ON d.carpark_id = c.carpark_id
        WHERE d.user_id = ?
        ORDER BY d.datetime DESC
        """
        try:
            self.cursor.execute(query, (user_id,))
            results = self.cursor.fetchall()

            return [
                {"carparkID": row[0], "address": row[1], "datetime": row[2]}
                for row in results
            ]

        except Exception as e:
            print("Error occurred while fetching carpark history:", e)
            return []
