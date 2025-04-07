from server.DatabaseCtrl.DBFactory import DBFactory
from typing import Optional


class User:
    def __init__(self, user_id: Optional[int] = None, username: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None) -> None:
        """
        Initializes a User object with the given attributes.

        :param user_id: The ID of the user.
        :type user_id: Optional[int]

        :param username: The username of the user.
        :type username: Optional[str]

        :param email: The email address of the user.
        :type email: Optional[str]

        :param password: The password for the user.
        :type password: Optional[str]
        """
        self.user_id: Optional[int] = user_id
        self.username: Optional[str] = username
        self.email: Optional[str] = email
        self.password: Optional[str] = password  # Added password attribute
        self.logged_in: bool = False
        self.userQueries = DBFactory().create_db_connection("User")

    def is_logged_in(self) -> bool:
        """
        Checks if the user is logged in.

        :return: True if the user is logged in, False otherwise.
        :rtype: bool
        """
        return self.logged_in

    def login_user(self) -> None:
        """
        Logs the user in by setting the logged_in attribute to True.
        """
        self.logged_in = True

    def logout_user(self) -> None:
        """
        Logs the user out by setting the logged_in attribute to False.
        """
        self.logged_in = False

    def update_all_attributes(self, user_id: Optional[int] = None, username: Optional[str] = None, 
                               email: Optional[str] = None, password: Optional[str] = None, vehicle_type: Optional[str] = None, 
                               logged_in: Optional[bool] = None) -> None:
        """
        Updates the user's attributes.

        :param user_id: The new user ID.
        :type user_id: Optional[int]

        :param username: The new username.
        :type username: Optional[str]

        :param email: The new email address.
        :type email: Optional[str]

        :param password: The new password for the user.
        :type password: Optional[str]

        :param logged_in: Whether the user is logged in or not.
        :type logged_in: Optional[bool]
        """
        if user_id is not None:
            self.user_id = user_id
        if username is not None:
            self.username = username
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password  # Added password field
        if logged_in is not None:
            self.logged_in = logged_in

    def any_fields_empty(self) -> bool:
        """
        Checks if any of the important user fields are empty (None).

        :return: True if any of the user fields (user_id, username, email, password) are None, False otherwise.
        :rtype: bool
        """
        return any(
            attr is None for attr in [self.user_id, self.username, self.email]
        )

    def __repr__(self) -> str:
        """
        Represents the User object as a string.

        :return: String representation of the User object.
        :rtype: str
        """
        return (f"User(user_id={self.user_id}, username='{self.username}', email='{self.email}', "
                f"logged_in={self.logged_in})")
