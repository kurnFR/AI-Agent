from sqlalchemy import create_engine


class DatabaseManager:

    def __init__(self):

        self._engines = {}

    def register(self, name, connection_string):

        if name not in self._engines:

            self._engines[name] = create_engine(
                connection_string,
                pool_pre_ping=True
            )

    def engine(self, name):

        return self._engines[name]