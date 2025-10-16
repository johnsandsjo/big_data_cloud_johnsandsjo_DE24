import duckdb
import os

db_path = os.getenv("DUCKDB_PATH")

def query_job_listings(query = 'SELECT * FROM marts.mart_technical_jobs'):
    with duckdb.connect(db_path, read_only=True) as conn:
        return conn.query(f"{query}").df()