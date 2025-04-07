import sqlite3
import os

class DatabaseQueries:
    """
        A base class for managing SQLite database connections and executing queries.

        This class handles the connection setup to the SpotOn.db database, provides a 
        cursor for executing queries, and includes a method to cleanly close the connection.
    """
    def __init__(self):
        """
        Initializes a connection to the SQLite database.

        Establishes a connection to 'SpotOn.db' located in the same directory as the script.

        If successful, a database cursor is created for executing SQL queries.

        On failure, sets both connection and cursor to None and prints an error message.
    """
        try:
            
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, 'SpotOn.db')
            
            # Initialize the connection
            self.connection = sqlite3.connect('SpotOn.db', check_same_thread=False)
            # Create the cursor
            self.cursor = self.connection.cursor()
            print("Database connection established")
        except sqlite3.Error as e:
            print(f"Database connection failed: {e}")
            self.connection = None
            self.cursor = None

    def close_connection(self):
        """
        Closes the database cursor and connection if they are active.

        This method ensures resources are properly released when the database is no longer needed.
    """
        # Close cursor and connection
        if self.connection:
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            print("Connection closed")

if __name__ == '__main__':
    db = DatabaseQueries()
    if db.connection:
        print("Worked")
    db.close_connection()
    




