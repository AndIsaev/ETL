from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sub_queries import load_person_id, big_request
from state import JsonFileStorage, State


class PostgresLoader:
    def __init__(self, pg_conn: _connection, state_key='key'):
        self.conn = pg_conn
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        self.key = state_key
        self.state_key = State(JsonFileStorage('postgres_data.txt')).get_state(state_key)
        self.data = []

    def load_film_work_id(self) -> str:
        """Вложенный запрос на получение фильмов"""
        load_film_id = f'''select distinct fw.id
                            from content.film_work as fw
                            left join content.person_film_work as pfw on pfw.film_work_id = fw.id
                            where pfw.person_id in ({load_person_id})
                            group by fw.id
                            '''
        if self.state_key is None:
            return load_film_id
        inx = load_film_id.rfind(f'where pfw.person_id in ({load_person_id})')
        return f"{load_film_id[:inx]} and updated_at > '{self.state_key}' {load_film_id[inx:]}"

    def loader_from_postgresql(self) -> list:
        """
        Главный запрос на получение данных из бд
        """

        full_load = f"""
            select
            fw.id,
            fw.title,
            fw.description,
            fw.rating as imdb_rating,
            {big_request}
            from content.film_work fw
            left join content.person_film_work as pfw on pfw.film_work_id = fw.id
            left join content.person as p on p.id = pfw.person_id
            left join content.genre_film_work gfw on gfw.film_work_id = fw.id
            left join content.genre g on g.id = gfw.genre_id
            where fw.id in ({self.load_film_work_id()})
            group by fw.id
            order by fw.updated_at;
"""

        self.cursor.execute(full_load)

        columns = [d[0] for d in self.cursor.description]
        data = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        return data
