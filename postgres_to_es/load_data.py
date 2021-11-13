import psycopg2
import logging
from datetime import datetime
from contextlib import closing
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from config import dsl, es_conf
from postgres_loader import PostgresLoader
from services import backoff
from elasticsearch_loader import ElasticSearchLoader


logger = logging.getLogger('LoaderStart')


def load_from_postgres(pg_conn: _connection) -> list:
    postgres_loader = PostgresLoader(pg_conn)
    data = postgres_loader.loader_from_postgresql()
    return data


if __name__ == '__main__':
    @backoff()
    def query_postgres() -> list:
        with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
            logger.info(f'{datetime.now()}\n\nустановлена связь с PostgreSQL. Начинаем загрузку данных')
            load_pq = load_from_postgres(pg_conn)
        return load_pq

    def save_elastic() -> None:
        logger.info(f'{datetime.now()}\n\nустановлена связь с ElasticSearch. Начинаем загрузку данных')
        ElasticSearchLoader(es_conf).create_index('movies')
        ElasticSearchLoader(es_conf).load_data_to_elasticsearch(query_postgres())

    save_elastic()
