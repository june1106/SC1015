from server.entity.User import User

class UserCtrl:
    def __init__(self, user: User) -> None:
        """
        Initialize UserCtrl with a User instance.

        :param user: The User instance to manage.
        :type user: User
        """
        self.user = user

    def update_username(self, username: str) -> None:
        """
        Update the user's username.

        :param username: The new username.
        :type username: str
        """
        self.user.username = username

    def update_name(self, name: str) -> None:
        """
        Update the user's name.
        
        :param name: The new name.
        :type name: str
        """
        self.user.name = name

    def update_email(self, email: str) -> None:
        """
        Update the user's email address.

        :param email: The new email address.
        :type email: str
        """
        self.user.email = email

    def update_user_details(self, **kwargs: dict) -> None:
        """
        Update multiple user attributes at once.

        :param kwargs: Key-value pairs of user attributes and their new values.
        :raises ValueError: If an attribute does not exist on the user.
        :type kwargs: dict
        """
        for key, value in kwargs.items():
            if hasattr(self.user, key):
                setattr(self.user, key, value)
            else:
                raise ValueError(f"User has no attribute '{key}'")

    def get_user_info(self) -> str:
        """
        Get a string representation of the user.

        :return: A string representing the user.
        :rtype: str
        """
        return str(self.user)