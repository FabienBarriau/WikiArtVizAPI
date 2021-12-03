import os
from typing import Optional
from pymongo import MongoClient
import json

class MongoConfig:

    def __init__(self, database: str, host: str, port: str, username: str, password: str):
        self.database = database
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def __str__(self):
        return f'database: {self.database}\n' \
        f'host: {self.host}\n' \
        f'port: {self.port}\n' \
        f'username: {self.username}\n' \
        f'password: {"".join(["x" for _ in self.password])}\n'

class MongoDatabase:

    def __init__(self, config: MongoConfig):
        self.config = config
        self.client: Optional[MongoClient]=None

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self):
        self.client.close()

    def __str__(self):
        return f'{self.config} \n' \
        f'connected: {self.client is not None}\n'

    def _connect(self):
        self.client = MongoClient(host=self.config.host, port=self.config.port,  authSource=self.config.database,
                                  username=self.config.username, password=self.config.password)
        self.verify_connection()

    def verify_connection(self):
        if self.client is None:
            raise RuntimeError('Not connected')
        self.client.server_info()

    def get_db(self):
        return self.client[self.database]

def get_db_config(force_env: bool = False) -> dict:
    config = {}
    if ('db_config.json' in os.listdir('./config')) and not force_env:
        with open('./config/db_config.json') as json_file:
            config = json.load(json_file)
    else:
        for variable in ['DATABASE', 'DATABASE_PORT', 'DATABASE_HOST', 'DATABASE_USERNAME', 'DATABASE_PASSWORD']:
            config[variable] = os.getenv(variable)
    config['DATABASE_PORT'] = int(config['DATABASE_PORT'])
    return config

def get_mongo_database(force_env: bool = False):
    db_config = get_db_config(force_env)
    with MongoDatabase(db_config) as mongo_database:
        yield mongo_database


