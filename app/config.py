import os


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    driver = os.getenv("DB_DRIVER", "sqlite").lower()
    if driver in ("mysql", "mysql+pymysql"):
        host = os.getenv("MYSQL_HOST", "127.0.0.1")
        port = os.getenv("MYSQL_PORT", "3306")
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASSWORD", "")
        database = os.getenv("MYSQL_DATABASE", "inventory_db")
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    return "sqlite:///inventory.db"
