from server.entity.Destination import Destination

class DestinationCtrl:
    """
    A class to control the creation, deletion, and modification of destinations for users.
    """

    def create_destination(self, user_id: int, carpark_id: str, datetime: str) -> Destination:
        """
        Creates a new destination for a user.

        :param user_id: The ID of the user for whom the destination is created.
        :type user_id: str

        :param carpark_id: The ID of the carpark to be included in the destination.
        :type carpark_id: str

        :param datetime: The datetime the destination is scheduled for, in YYYY-MM-DD-HH-MM-SS format.
        :type datetime: str

        :return: The created Destination object.
        :rtype: Destination
        """
        destination = Destination().create_new_destination(user_id, carpark_id, datetime)
        return destination

    def delete_destination(self, user_id: int, carpark_id: str, datetime: str) -> None:
        """
        Deletes a destination for a user.

        :param user_id: The ID of the user whose destination will be deleted.
        :type user_id: int

        :param datetime: The datetime of the destination to delete, in YYYY-MM-DD-HH-MM-SS format.
        :type datetime: str

        :return: None
        :rtype: None
        """
        Destination().delete_destination(user_id, datetime)
