import pandas as pd
from sqlalchemy import create_engine, text, URL


class MysqlAdapter:
    def __init__(self, host: str, user: str, password: str, database: str = None, port: int = 3306):
        connection_string = URL.create(
            "mysql+pymysql",
            username=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        
        self.__engine = create_engine(
            connection_string,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
    
    def execute(self, query: str, params: dict = None) -> list[tuple] | None:
        with self.__engine.connect() as connection:
            return connection.execute(text(query), params or {}).fetchall()
    
    def to_pandas(self, query: str, params: dict = None) -> pd.DataFrame | None:
        with self.__engine.connect() as connection:
            return pd.read_sql(text(query), connection, params=params)