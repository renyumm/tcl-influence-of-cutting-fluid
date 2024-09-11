'''
LastEditors: renyumm strrenyumm@gmail.com
Date: 2024-09-09 10:45:45
LastEditTime: 2024-09-11 14:56:24
FilePath: /tcl-influence-of-cutting-fluid/src/utils/connector.py
'''
from sqlalchemy import create_engine
import pandas as pd

class Connector(object):
    def __init__(self, yaml_config):
        self.config = yaml_config
        self.structure_db = ['clickhouse']
        self.dbtype = yaml_config['type']
        self.host = yaml_config['host']
        self.port = yaml_config['port']
        self.engine = self.connect()


    def connect(self):
        if self.dbtype in self.structure_db:
            self.database = self.config['database']
            self.username = self.config['username']
            self.password = self.config['password']
            connection = f'{self.dbtype}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
            return create_engine(connection)
        
    def dispose(self):
        if self.dbtype in self.structure_db:
            self.engine.dispose()
            return True
    
    def get_data(self, query):
        if self.dbtype in self.structure_db:
            data = pd.read_sql(query, self.engine)
            return data
            