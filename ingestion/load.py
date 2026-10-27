import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
load_dotenv()

JSON_FILE = Path(__file__).resolve().parent.parent / "data" / "cleaned" / "all_cars.json"

with open(JSON_FILE, encoding="utf-8") as f:
    rows = json.load(f)

print(f"read {len(rows)} rows from {JSON_FILE}")

INSERT_SQL = """
    INSERT INTO raw.car_listings (
        listing_id, brand, model, year, price, 
        mileage_km, region_slug, url, source_file, scraped_at
    ) VALUES (
        %(listing_id)s, %(brand)s, %(model)s, %(year)s, %(price)s,
        %(mileage_km)s, %(region_slug)s, %(url)s, %(source_file)s, %(scraped_at)s
    )
    ON CONFLICT (listing_id, scraped_at) DO NOTHING
"""

with psycopg.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
) as conn:
    with conn.cursor() as cur:
        cur.executemany(INSERT_SQL, rows)
        print(f"inserted {cur.rowcount}")

    print(conn.execute("SELECT count(*) FROM raw.car_listings").fetchone())