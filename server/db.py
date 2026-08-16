import os
import pg8000
from dotenv import load_dotenv

# Load env files relative to this file's directory
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

def get_db_connection():
    """
    Creates and returns a connection to the PostgreSQL database using standard DB-API 2.0.
    """
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        from urllib.parse import urlparse
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgres://", 1)
        parsed = urlparse(db_url)
        return pg8000.connect(
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            database=parsed.path.lstrip('/'),
            port=parsed.port or 5432
        )
        
    return pg8000.connect(
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_DATABASE", "theatre_tickets"),
        port=int(os.getenv("DB_PORT", "5432"))
    )

def query_as_dicts(conn, sql, params=None):
    """
    Executes a query and returns the rows as a list of dictionaries with column names as keys.
    """
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        # Check if description is present (queries that return rows)
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        return []
    finally:
        cursor.close()

def test_connection():
    try:
        conn = get_db_connection()
        res = query_as_dicts(conn, "SELECT version() as ver;")
        print("Database connection test succeeded:", res)
        conn.close()
        return True
    except Exception as e:
        print("Database connection test failed:", e)
        return False
