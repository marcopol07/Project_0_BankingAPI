import psycopg2
from psycopg2 import OperationalError


def create_connection():
    try:
        conn = psycopg2.connect(
            # This has been removed for clone to public GitHub
        )
        return conn
    except OperationalError as e:
        print(f"{e}")
        return conn


connection = create_connection()
