from mysql import connector
import time


def init_db(app):
    conn = connector.connect(
        user='root',
        password=str(app.config.get('DB_ROOT_PASSWORD')),
        host=app.config.get('DB_HOST'),
        database=''
    )

    with app.open_resource('schema.sql') as schema:
        cursor = conn.cursor()
        cursor.execute(schema.read())
        cursor.close()
    conn.close()
    time.sleep(0.5)


class Database:
    def __init__(self, config):
        self._cnx = connector.connect(
            user=config.get('DB_USER'),
            password=config.get('DB_PASSWORD'),
            host=config.get('DB_HOST'),
            database=config.get('DB_DATABASE')
        )

    def get_connection(self):
        return self._cnx

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cnx.close()
