import pandas as pd
from trino.dbapi import connect

class TrinoAdapter:
    def __init__(self, host: str, port: int, user: str):
        self.host = host
        self.port = port
        self.user = user
        self.conn = connect(host=self.host, port=self.port, user=self.user)

    def execute(self, query: str):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def to_pandas(self, query: str):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(rows, columns=columns)
