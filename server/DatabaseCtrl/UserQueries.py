import sqlite3
from server.DatabaseCtrl.DatabaseQueries import DatabaseQueries
from server.entity.User import User

class UserQueries(DatabaseQueries):
    def __init__(self):
        """
        Initializes the UserQueries object by calling the parent constructor to establish a connection to the database.
        """
        # Initialize the connection
        super().__init__()

    def close_connection(self):
        """
        Closes the cursor and database connection.

        :return: None
        """
        # Close cursor and connection
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Connection closed")

    def does_username_or_email_exist(self, username: str, email: str) -> bool:
        """
        Checks if the username/email exists in the system.

        :param username: The username to check.
        :type username: str
        :param email: The email to check.
        :type email: str

        :return: True if the username or email exists, False otherwise.
        :rtype: bool
        """
        select_query = """
        SELECT user_id FROM Users 
        WHERE (username = ? OR email = ?) 
        """
        self.cursor.execute(select_query, (username, email,))
        result = self.cursor.fetchone()

        return result is not None

    def insert_new_user(self, username: str, email: str, password: str) -> int:
        """
        Insert new user info into the Users table.

        :param username: The username for the new user.
        :type username: str
        :param email: The email for the new user.
        :type email: str
        :param password: The password for the new user.
        :type password: str

        :return: The user ID of the newly inserted user, or 0 if the username/email already exists.
        :rtype: int
        """
        if not self.does_username_or_email_exist(username, email):
            insert_query = """
            INSERT INTO Users(username, email, password)
            VALUES (?, ?, ?)
            """
            self.cursor.execute(insert_query, (username, email, password))
            self.connection.commit()
            return self.cursor.lastrowid
        return 0

    def logging_in_user(self, user_id: int) -> dict:
        """
        Called only when a user logs in. Retrieves user details for a user logging in.

        :param user_id: The user ID of the user logging in.
        :type user_id: int

        :return: A dictionary containing the user ID, username, email, and login status, or None if the user does not exist.
        :rtype: dict or None
        """
        query = """
            SELECT username, email 
            FROM Users 
            WHERE user_id = ?
        """
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()

        if result:
            return {
                'user_id': user_id,
                'username': result[0],
                'email': result[1],
                'logged_in': True
            }
        return None

    def find_user_id(self, username: str, email: str, password: str) -> int:
        """
        Find existing user ID for a user based on their username, email, and password.

        :param username: The username of the user.
        :type username: str
        :param email: The email of the user.
        :type email: str
        :param password: The password of the user.
        :type password: str

        :return: The user ID if the user exists and the password is correct, or None if no matching user is found.
        :rtype: int or None
        """
        select_query = """
        SELECT user_id FROM Users 
        WHERE (username = ? OR email = ?) 
        AND password = ?
        """
        self.cursor.execute(select_query, (username, email, password))
        result = self.cursor.fetchone()

        return result[0] if result else None

    def delete_user(self, username: str, email: str, password: str) -> bool:
        """
        Delete a user from the Users table based on their username, email, and password.

        :param username: The username of the user to delete.
        :type username: str
        :param email: The email of the user to delete.
        :type email: str
        :param password: The password of the user to delete.
        :type password: str

        :return: True if the user was deleted successfully, False if the user does not exist or the password is incorrect.
        :rtype: bool
        """
        user_id = self.find_user_id(username, email, password)
        if user_id is not None:
            delete_query = """
            DELETE FROM Users WHERE user_id = ?
            """
            self.cursor.execute(delete_query, (user_id,))
            self.connection.commit()
            return True
        return False

    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieve a user's details by their user id.

        :param user_id: The user ID to retrieve details for.
        :type user_id: int

        :return: A User object containing the user's details, or None if the user does not exist.
        :rtype: User or None
        """
        query = """
            SELECT username, email 
            FROM Users 
            WHERE user_id = ?
        """
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()

        if result:
            return User(user_id=user_id, username=result[0], email=result[1])
        return None
    
    def update_user_password(self, username: str, email: str, new_password: str) -> None:
        """
        Updates the password of an existing user.

        :param username: The username of the user whose password is being updated.
        :type username: str
        :param email: The email of the user whose password is being updated.
        :type email: str
        :param new_password: The new password to set for the user.
        :type new_password: str

        :return: None
        """
        query = """
        UPDATE Users
        SET password = ?
        WHERE username = ? AND email = ?
        """
        self.cursor.execute(query, (new_password, username, email))
        self.connection.commit()
        return self.cursor.rowcount
        
    def run_tests(self):
        """
        Runs a set of test cases to validate the functionality of the UserQueries methods.

        :return: None
        """
        def terminate_program(message: str):
            """Print error message and raise an exception instead of exiting."""
            raise Exception(message)

        db = UserQueries()

        if not db.connection:
            terminate_program("Failed to connect to the database")
        else:
            print("Successfully connected to the database")

        # Test Case 1: Add a new user
        user_id = db.insert_new_user('test1', 'test1@example.com', 'password')
        assert user_id != 0, "Failed to add new user"
        print("Test 1 passed")

        # Test Case 2: Attempt to add the same user again
        result = db.insert_new_user('test1', 'test1@example.com', 'password')
        assert result == 0, "Should have returned 0 for duplicate user"
        print("Test 2 passed")

        # Test Case 3: Find user ID
        found_id = db.find_user_id("test1", "test1@example.com", "password")
        assert found_id is not None, "User ID not found"
        print("Test 3 passed")

        # Test Case 4: Find user ID with wrong password
        found_id = db.find_user_id("test1", "test1@example.com", "wrongPassword")
        assert found_id is None, "Wrong password should return None"
        print("Test 4 passed")

        # Test Case 5: Attempt to delete user with incorrect password
        result = db.delete_user('test1', 'test1@example.com', 'wrongPassword')
        assert not result, "Wrong password should not allow deletion"
        print("Test 5 passed")

        # Test Case 6: Successfully delete user
        result = db.delete_user('test1', 'test1@example.com', 'password')
        assert result, "User deletion failed"
        print("Test 6 passed")

        # Test Case 7: Ensure user is deleted
        found_id = db.find_user_id("test1", "test1@example.com", "password")
        assert found_id is None, "User should not exist after deletion"
        print("Test 7 passed")

        db.close_connection()

if __name__ == '__main__':
    db = UserQueries()
    db.run_tests()
