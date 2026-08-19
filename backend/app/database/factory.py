from app.config import DATABASE_URL
from app.database.manager import DatabaseManager

manager = DatabaseManager()

try:
    if DATABASE_URL:
        manager.register(
            "postgres",
            DATABASE_URL
        )
except Exception:
    pass