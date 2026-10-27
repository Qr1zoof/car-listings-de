CREATE TABLE raw.car_listings (
    listing_id BIGINT,
    brand TEXT,
    model TEXT,
    year INTEGER,
    price INTEGER,
    mileage_km INTEGER,
    region_slug TEXT,
    url TEXT,
    source_file TEXT NOT NULL,
    scraped_at TIMESTAMPTZ NOT NULL,

    PRIMARY KEY (listing_id, scraped_at)
);