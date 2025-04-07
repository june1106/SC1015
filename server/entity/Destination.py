from server.DatabaseCtrl.DBFactory import DBFactory
from typing import Optional, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Destination:
    """
    Represents a destination with its properties and database interaction methods.

    :param user_id: The ID of the user associated with the destination.
    :type user_id: int

    :param carpark_id: The ID of the carpark in the destination.
    :type carpark_id: str
    
    :param datetime: The datetime of the destination.
    :type datetime: str

    :param db: An instance of the DestinationQueries class for database operations.
    :type db: DestinationQueries
    """
    
    def __init__(self, user_id: int = 0, carpark_id: str = '', datetime: str = '') -> None:
        """
        Initializes a Destination object with the given properties.

        :param user_id: The ID of the user associated with the destination. Defaults to 0.
        :type user_id: int, optional

        :param carpark_id: The ID of the carpark in the destination. Defaults to an empty string.
        :type carpark_id: str, optional

        :param datetime: The datetime of the destination. Defaults to an empty string.
        :type datetime: str, optional
        """
        self.user_id = user_id
        self.carpark_id = carpark_id
        self.datetime = datetime
        self.db = DBFactory().create_db_connection("Destination")

    def fetch_destination_from_db(self, user_id: int) -> Optional[Dict]:
        """
        Fetches a destination from the database for a specific user.

        :param user_id: The ID of the user for whom to fetch the destination.
        :type user_id: int
        
        :return: The fetched destination data as a dictionary, or None if no data is found.
        :rtype: dict or None
        """
        try:
            data = self.db.fetch_destination_user_id(user_id)
            return data if data else None
        except Exception as e:
            logging.error(f"Error fetching destination from DB: {e}")
            return None

    def create_new_destination(self, user_id: int, carpark_id: str, datetime: str) -> Optional['Destination']:
        """
        Creates a new destination and inserts it into the database.

        :param user_id: The ID of the user associated with the destination.
        :type user_id: int

        :param carpark_id: The ID of the carpark in the destination.
        :type carpark_id: str

        :param datetime: The datetime of the destination.
        :type datetime: str

        :return: The created Destination object if successful, or None if the insertion failed.
        :rtype: Destination or None
        """
        try:
            id = self.db.insert_new_destination(user_id, carpark_id, datetime)
            logging.info(f"Inserted destination ID: {id}, type: {type(id)}")
            
            if id == 0:
                return None

            self.user_id = user_id
            self.carpark_id = carpark_id
            self.datetime = datetime
            return self
        except Exception as e:
            logging.error(f"Error creating new destination: {e}")
            return None

    def delete_destination(self, user_id: int, datetime: str) -> bool:
        """
        Deletes a destination from the database.

        :param user_id: The ID of the user associated with the destination.
        :type user_id: int

        :param datetime: The datetime of the destination to delete.
        :type datetime: str

        :return: True if deletion was successful, False otherwise.
        :rtype: bool
        """
        try:
            result = self.db.delete_inserted_destination(user_id, datetime)
            if result:
                logging.info(f"Destination for user {user_id} on {datetime} deleted successfully.")
                return True
            else:
                logging.warning(f"Failed to delete destination for user {user_id} on {datetime}.")
                return False
        except Exception as e:
            logging.error(f"Error deleting destination from DB: {e}")
            return False
