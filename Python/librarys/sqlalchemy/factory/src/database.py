from abc import ABC, abstractmethod

import polars as pl
from dependency_injector import containers, providers
from loguru import logger
from sqlalchemy import create_engine


class DatabaseConnector(ABC):
    @abstractmethod
    def connect(self):
        self.engine = None

    @abstractmethod
    def execute(self, query: str) -> pl.DataFrame | None:
        result = None

        try:
            with self.engine.connect() as connection:
                result = pl.read_database(query=query, connection=connection)
        except Exception as e:
            logger.error(f"Error while executing query: {e}")

        return result


class MysqlConnector(DatabaseConnector):
    def __init__(self, config: dict):
        self.connect_arg = config
        self.engine = self.connect()

    def connect(self):
        engine = create_engine("mysql+pymysql://:@", connect_args=self.connect_arg)

        return engine


class OracleConnector(DatabaseConnector):
    def __init__(self, config: dict):
        self.connect_arg = config
        self.engine = self.connect()

    def connect(self):
        engine = create_engine("oracle+oracledb://:@", connect_args=self.connect_arg)

        return engine


# class PostgresConnector(DatabaseConnector):
#     def __init__(self, config: dict):
#         self.connect_arg = config
#         self.engine = self.connect()

#     def connect(self):
#         engine = create_engine("postgresql://:@", connect_args=self.connect_arg)

#         return engine


class DatabaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    mysql_connector = providers.Singleton(MysqlConnector, config=config.mysql)
    oracle_connector = providers.Singleton(OracleConnector, config=config.oracle)
    # postgres_connector = providers.Singleton(PostgresConnector, config=config.postgres)
