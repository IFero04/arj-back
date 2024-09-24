import psycopg2
import os
from urllib.parse import urlparse

# Fetch the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

def connect_to_db():
    try:
        # Parse the URL to ensure correctness
        result = urlparse(DATABASE_URL)
        if not all([result.scheme, result.hostname, result.path, result.username, result.password]):
            raise ValueError("Invalid DATABASE_URL format")

        # Connect to PostgreSQL using the database URL
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        # Execute a simple query to verify the connection
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"Connected to PostgreSQL database. Version: {db_version[0]}")

        cursor.close()
        connection.close()

    except Exception as error:
        print(f"Error connecting to the database: {error}")

if __name__ == "__main__":
    connect_to_db()
