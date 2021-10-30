import csv
import json
import psycopg2
from elasticsearch import Elasticsearch
from postgres_to_es.create_index import create_index_es

# создаем экземпляр Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# создаем экземпляр подключения к PostgreSQL
connection = psycopg2.connect(
    database='yandex',
    user='postgres',
    password='postgres',
    host='localhost',
    port=5432
)

psycopg2_cursor = connection.cursor()


class PostgreSQL:
    def __init__(self, psycopg2_cursor, es_connect):
        self.psycopg2_cursor = psycopg2_cursor
        self.es_connect = es_connect

    def get_table_from_psycopg2(self):
        """Get table with data from sqlite."""
        query = """select id, title from content.film_work limit 5;"""
        psycopg2_cursor.execute(query)
        with open("output.csv", "w") as out_csv_file:
            csv_out = csv.writer(out_csv_file)
            csv_out.writerow([d[0] for d in psycopg2_cursor.description])
            for row in psycopg2_cursor:
                csv_out.writerow(row)

    def csv_to_json(self):
        jsonArray = []

        # read csv file
        with open("output.csv", encoding='utf-8') as csvf:
            # load csv file data using csv library's dictionary reader
            csvReader = csv.DictReader(csvf)

            # convert each csv row into python dict
            for row in csvReader:
                # add this python dict to json array
                jsonArray.append(row)

        # convert python jsonArray to JSON String and write to file
        with open("output.json", 'w', encoding='utf-8') as jsonf:
            jsonString = json.dumps(jsonArray, indent=4)
            jsonf.write(jsonString)

    def bulk_data_to_elastic(self):
        """
        send data to elastic.
        """
        data = []
        with open("output.json", 'r') as test:
            d = json.load(test)
            for i in d:
                data.append({"create": {"_index": "movies", "_id": i['id']}})
                data.append(i)

        self.es_connect.bulk(index='movies', body=data)


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('It could not connect!')
    return _es
#
#


# def create_doc(data):
#     id_data = data.get('id')
#     insert_data = es.index(index='movies', id=id_data, document=data)
#     return insert_data


if __name__ == '__main__':
    es = connect_elasticsearch()
    create_index_es(es, index_name='movies')
    pos = PostgreSQL(psycopg2_cursor, es)
    pos.get_table_from_psycopg2()
    pos.csv_to_json()
    pos.bulk_data_to_elastic()


    # create_doc(data)

    # bulk_data_to_elastic(es, "movies", result)
