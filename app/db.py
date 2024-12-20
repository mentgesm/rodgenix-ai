import pymysql
import os

# MariaDB Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "mentges99"),
    "database": os.getenv("DB_NAME", "rodgenix"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

def db_connect():
    """Connect to the MariaDB database."""
    return pymysql.connect(**DB_CONFIG)
