import duckdb as ddb

def verify_load(con, table_name, before_count, source_path):
    loaded_count = con.execute(f"SELECT COUNT(*) FROM {source_path}").fetchone()[0]
    after_count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    expected = before_count + loaded_count
    assert after_count == expected, (
        f"Load verification failed for {table_name}: "
        f"Expected {expected} rows ({before_count} existing + {loaded_count} loaded), "
        f"found {after_count}"
    )

con = ddb.connect('catawba.db')

result = con.execute(
    "SELECT table_name FROM information_schema.tables WHERE table_name = 'raw_readings'").fetchone()[0]


if result is None: 
    con.execute("CREATE TABLE raw_readings AS SELECT * FROM 'data/long_format.parquet'")
    verify_load(con, 'raw_readings', 0, 'data/long_format.parquet')
else:
    con.execute("CREATE OR REPLACE TABLE raw_readings AS SELECT *, CURRENT_TIMESTAMP AS date_loaded FROM 'data/long_format.parquet'")

assert con.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'raw_readings' AND column_name = 'date_loaded'").fetchone() is not None, (
        "Column date_loaded does not exist")