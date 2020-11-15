import os
from pymongo import MongoClient
import json
from enum import Enum


def get_config(force_env: bool = False) -> dict:
    config = {}
    if ('db_config.json' in os.listdir('./config')) and not force_env:
        with open('./config/db_config.json') as json_file:
            config = json.load(json_file)
    else:
        for variable in ['DATABASE', 'DATABASE_PORT', 'DATABASE_HOST', 'DATABASE_USERNAME', 'DATABASE_PASSWORD']:
            config[variable] = os.getenv(variable)
    config['DATABASE_PORT'] = int(config['DATABASE_PORT'])
    return config


class Metric(Enum):
    COLOR = 'color-encoding'
    CONTENT = 'encoding'


class Database:

    def __init__(self, database: str, host: str, port: str, username: str, password: str):
        self.database = database
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        self.client = MongoClient(host=self.host, port=self.port,  authSource=self.database,
                                  username=self.username, password=self.password)
        self.verify_connection()

    def verify_connection(self):
        if self.client is None:
            raise RuntimeError('Not connected')
        self.client.server_info()

    def get_db(self):
        return self.client[self.database]

    def get_distance_for_art(self, art_id: str, metric: Metric) -> dict:
        return self.client[self.database]['distance'].find_one({'_id': art_id}, [metric.value])[metric.value]

    def get_arts_ids(self, filters: dict = None) -> list:
        if filters is None:
            return []
        else:
            mongo_filter = {}
            for key, value in filters.items():
                if value is not None:
                    mongo_filter[key] = {"$in": value}
            ids_dict = list(self.client[self.database]['paintings'].find(mongo_filter, []))
            return [id_dict["_id"] for id_dict in ids_dict]

    def get_art_info(self, art_id: str, infos: list) -> dict:
        return self.client[self.database]['paintings'].find_one({'_id': art_id}, infos)

    def get_arts_info(self, art_ids: list, infos: list) -> list:
        return [self.get_art_info(art_id, infos) for art_id in art_ids]

    def get_categories(self, label: list):
        if label:
            return self.client[self.database]['categories'].find_one({}, label)
        else:
            return self.client[self.database]['categories'].find_one({})




