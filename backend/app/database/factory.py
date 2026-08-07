from app.database.manager import DatabaseManager

from app.settings.postgres import DATABASE_URL


manager = DatabaseManager()

manager.register(
    "postgres",
    DATABASE_URL
)