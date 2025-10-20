from pathlib import Path
import duckdb

# data warehouse directory
DB_PATH = Path("/app/data_warehouse/job_ads.duckdb")
 
def query_job_listings(query='SELECT * FROM marts.mart_technical_jobs'):
    with duckdb.connect(DB_PATH, read_only=True) as conn:
        return conn.query(f"{query}").df()


