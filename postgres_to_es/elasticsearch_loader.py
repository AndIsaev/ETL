import json
import logging
from datetime import datetime
from elasticsearch import Elasticsearch
from esindex import CINEMA_INDEX_BODY
from services import backoff
from state import State, JsonFileStorage

logger = logging.getLogger('ESLoader')


class ElasticSearchLoader:
    def __init__(self, host: list, state_key='key'):
        self.client = Elasticsearch(host)
        self.data = []
        self.key = state_key

    @backoff()
    def create_index(self, index: str) -> None:
        """
        Создаем индекс для Elasticsearch.
        """
        if not self.client.indices.exists(index):
            self.client.indices.create(index=index, ignore=400, body=CINEMA_INDEX_BODY)
            logger.warning(f'{datetime.now()}\n\nиндекс {index} создан')
        logger.warning(f'{datetime.now()}\n\nиндекс {index} был создан ранее')

    @backoff()
    def bulk_data_to_elasticsearch(self) -> None:
        self.client.bulk(index='movies', body=self.data, refresh=True)

    def load_data_to_elasticsearch(self, query) -> None:
        """
        Загружаем данные пачками в Elasticsearch.
        """
        data_json = json.dumps(query)
        load_json = json.loads(data_json)
        count = len(load_json)
        i = 0

        while count != 0:
            if count >= 50:
                for j in range(i, i + 50):
                    self.data.append({"create": {"_index": "movies", "_id": load_json[i]['id']}})
                    self.data.append(load_json[i])
                    i += 1
                self.bulk_data_to_elasticsearch()
                self.data.clear()
                count -= 50
            else:
                for j in range(i, i + count):
                    self.data.append({"create": {"_index": "movies", "_id": load_json[i]['id']}})
                    self.data.append(load_json[i])
                    i += 1
                self.bulk_data_to_elasticsearch()
                count -= count
                self.data.clear()
        State(JsonFileStorage('postgres_data.txt')).set_state(str(self.key), value=str(datetime.now()))
