from mysql import connector


class Database:
    def __init__(self):
        self.__cnx = connector.connect(database="invoice_store")

    def get_connection(self):
        return self.__cnx

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cnx.close()
