from datetime import datetime
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from query import main_query
from state import JsonFileStorage, State


class PostgresLoader:
    def __init__(self, pg_conn: _connection, state_key='key'):
        self.conn = pg_conn
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        self.key = state_key
        self.state_key = State(JsonFileStorage('postgres_data.txt')).get_state(state_key)
        self.batch = 100
        self.data = []
        self.count = 0

    def get_state_key(self):
        """
        Определяем какую дату будем использовать для сравнения при запросе.
        """
        if self.state_key is None:
            return datetime(2005, 7, 14, 12, 30)
        return self.state_key

    def loader_from_postgresql(self) -> list:
        """
        Главный запрос на получение данных из бд.
        """
        self.cursor.execute(main_query % self.get_state_key())
        records = self.cursor.fetchall()
        self.conn.close()
        return records
