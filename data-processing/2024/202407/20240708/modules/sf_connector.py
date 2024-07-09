from snowflake.snowpark import Session


class SfConnector:
    def __init__(
        self, account, user, password, role, warehouse, database, schema
    ) -> None:
        self.connection_parameters = {
            "account": account,
            "user": user,
            "password": password,
            "role": role,
            "warehouse": warehouse,
            "database": database,
            "schema": schema,
        }

    def get_session(self):
        yield Session.builder.configs(self.connection_parameters).create()
