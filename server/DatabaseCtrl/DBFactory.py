class DBFactory():
    def __init__(self) -> None:
        self.db = None

    def create_db_connection(self, type: str) -> object:
        """
            Create a database connection based on types provided

            :param type: The type of connection required. It can be one of the following:
                 'Destination', 'User', or 'Carpark'.
            :type type: str

            :return: A connection object with queries to the database based on the specified type.
            :rtype: Connection Object

        """
        from server.DatabaseCtrl.DestinationQueries import DestinationQueries
        from server.DatabaseCtrl.UserQueries import UserQueries
        from server.DatabaseCtrl.CarparkQueries import CarparkQueries
        
        if type == "Destination":
            return DestinationQueries()
        elif type == "User":
            return UserQueries()
        elif type == "Carpark":
            return CarparkQueries()
        else:
            return None
