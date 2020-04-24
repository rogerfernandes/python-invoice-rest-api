from mysql import connector


class Database:
    def __init__(self, config):
        self.__cnx = connector.connect(
            user=config.get('DB_USER'),
            password=config.get('DB_PASSWORD'),
            host=config.get('DB_HOST'),
            database=config.get('DB_DATABASE')
        )

    def get_connection(self):
        return self.__cnx

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cnx.close()
