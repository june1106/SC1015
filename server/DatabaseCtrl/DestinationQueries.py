from server.DatabaseCtrl.DatabaseQueries import DatabaseQueries
import sqlite3
from typing import Optional

class DestinationQueries(DatabaseQueries):
    def __init__(self):
        super().__init__()

    def insert_new_destination(self, user_id: int, carpark_id: str, datetime: str) -> int:
        """
        Inserts a new destination into the database and returns the destination ID.

        :param user_id: ID of the user
        :param carpark_id: ID of the carpark
        :param datetime: datetime of destination
        :return: ID of the newly inserted destination
        """
        try:
            # Proceed with the insert
            insert_query = """
            INSERT INTO Destinations (user_id, carpark_id, datetime)
            VALUES (?, ?, ?)
            """

            # Execute the insert query
            self.cursor.execute(insert_query, (user_id, carpark_id, datetime))

            # Commit the transaction
            self.connection.commit()

            # Get the ID of the newly inserted destination
            return self.cursor.lastrowid

        except sqlite3.Error as e:
            # Rollback the transaction in case of error
            self.connection.rollback()
            print("Error occurred while inserting destination:", e)
            return 0

    def fetch_destination_user_id(self, user_id: int) -> dict:
        """
        Fetches a destination based on user ID.

        :param user_id: ID of the user
        :return: A dictionary containing destination and carpark details if found, an empty dictionary otherwise
        """
        select_query = """
        SELECT d.destination_id, d.user_id, d.carpark_id, d.datetime, c.address
        FROM Destinations d
        JOIN Carparks c ON d.carpark_id = c.carpark_id
        WHERE d.user_id = ?
        """

        try:
            # Execute the select query
            self.cursor.execute(select_query, (user_id,))

            # Fetch the result
            destination_row = self.cursor.fetchone()

            if destination_row:
                return {
                    'destination_id': destination_row[0],
                    'user_id': destination_row[1],
                    'carpark_id': destination_row[2],
                    'datetime': destination_row[3],
                    'address': destination_row[4],
                }
            return {}  # Return empty dictionary if no destination found

        except sqlite3.Error as e:
            print("Error occurred while fetching destination:", e)
            return {}

if __name__ == '__main__':
    db = DestinationQueries()

    # Corrected function call
    destination_id = db.insert_new_destination(123, "1100990", "2024-11-03")
    print("Inserted Destination ID:", destination_id)

    # Corrected function call
    destination_data = db.fetch_destination_user_id(123)
    print("Fetched Destination Data:", destination_data)

    db.close_connection()
