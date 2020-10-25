import os
from pymongo import MongoClient
import json


def get_config(force_env: bool = False):
    config = {}
    if ('config.json' in os.listdir('.')) and not force_env:
        with open('config.json') as json_file:
            config = json.load(json_file)
    else:
        for variable in ['DATABASE', 'DATABASE_PORT', 'DATABASE_HOST', 'DATABASE_USERNAME', 'DATABASE_PASSWORD']:
            config[variable] = os.getenv(variable)
    config['DATABASE_PORT'] = int(config['DATABASE_PORT'])
    return config


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




