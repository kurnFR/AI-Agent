from typing import Dict, List, Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class DatabaseManager:

    def __init__(self):

        self._engines: Dict[str, Engine] = {}

    def register(self, name: str, connection_string: str, **kwargs) -> Engine:

        if name not in self._engines:

            self._engines[name] = create_engine(
                connection_string,
                pool_pre_ping=True,
                **kwargs
            )

        return self._engines[name]

    def engine(self, name: str) -> Optional[Engine]:

        if name not in self._engines:
            raise KeyError(f"Database engine '{name}' is not registered.")
        return self._engines[name]

    def exists(self, name: str) -> bool:

        return name in self._engines

    def names(self) -> List[str]:

        return sorted(list(self._engines.keys()))

    def close_all(self) -> None:

        for name, engine in self._engines.items():
            try:
                engine.dispose()
            except Exception:
                pass
        self._engines.clear()