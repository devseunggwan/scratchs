from abc import ABC, abstractmethod

import polars as pl
from dependency_injector import containers, providers
from loguru import logger
from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.dialects.mysql import insert


class DatabaseConnector(ABC):
    @abstractmethod
    def connect(self):
        self.engine: Engine | None = None

    @abstractmethod
    def extract(self, query: str) -> pl.DataFrame | None:
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
        self.engine: Engine = self.connect()
        self.metadata: MetaData = MetaData()
        self.metadata.reflect(bind=self.engine)

    def connect(self):
        engine = create_engine("mysql+pymysql://:@", connect_args=self.connect_arg)

        return engine

    def get_table_metadata(self, table_name: str):
        return self.metadata.tables.get(table_name)

    def upsert_df(self, df: pl.DataFrame, table_name: str, batch_size=1000):
        records = df.to_dicts()
        total = len(records)
        table = self.get_table_metadata(table_name)

        for start in range(0, total, batch_size):
            end = min(start + batch_size, total)
            batch = records[start:end]

            if not batch:
                continue

            with self.engine.connect() as connection:
                stmt = insert(table).value(batch)
                update_dict = {
                    c.name: stmt.inserted[c.name]
                    for c in table.columns
                    if not c.primary_key
                }
                stmt = stmt.on_duplicate_key_update(**update_dict)
                connection.execute(stmt)


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
