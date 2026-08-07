import app.settings
import os
from urllib.parse import quote_plus

HOST = os.getenv("POSTGRES_HOST")
PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DATABASE = os.getenv("POSTGRES_DATABASE")

USER = quote_plus(os.getenv("POSTGRES_USER", ""))
PASSWORD = quote_plus(os.getenv("POSTGRES_PASSWORD", ""))

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{USER}:{PASSWORD}"
    f"@{HOST}:{PORT}"
    f"/{DATABASE}"
)