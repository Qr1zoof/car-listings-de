import json
import os

from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError

RAW_DIR = "data/raw"
OUTPUT_DIR = "data/cleaned"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "all_cars.json")


class CarListing(BaseModel):
    listing_id: int | None = None
    brand: str | None = None
    model: str | None = None
    year: int | None = None
    price: float | None = None
    mileage_km: float | None = None
    region_slug: str | None = None
    url: str | None = None
    source_file: str


def load_car_blocks(path: str) -> list[dict]:
    with open(path, "rb") as f:
        soup = BeautifulSoup(f, "lxml")
    tags = soup.find_all("script", attrs={"type": "application/ld+json"})
    cars = []
    for tag in tags:
        text = tag.string
        d = json.loads(text)
        if d.get("@type") == "Car":
            cars.append(d)
    return cars


def flatten_car(block: dict) -> dict:
    offers = block.get("offers") or {}
    brand = block.get("brand") or {}
    mileage = block.get("mileageFromOdometer") or {}
    url = offers.get("url")

    region_slug = None
    listing_id = None
    if url:
        parts = url.split("/")
        region_slug = parts[-4]
        last = parts[-1].replace(".html", "")
        if last.isdigit():
            listing_id = int(last)

    return {
        "listing_id": listing_id,
        "brand": brand.get("name"),
        "model": block.get("model"),
        "year": block.get("vehicleModelDate"),
        "price": offers.get("price"),
        "mileage_km": mileage.get("value"),
        "region_slug": region_slug,
        "url": url,
    }


def extract_and_validate(data: dict, source_file: str) -> CarListing | None:
    try:
        return CarListing(
            listing_id=data.get("listing_id"),
            brand=data.get("brand"),
            model=data.get("model"),
            year=data.get("year"),
            price=data.get("price"),
            mileage_km=data.get("mileage_km"),
            region_slug=data.get("region_slug"),
            url=data.get("url"),
            source_file=source_file,
        )
    except ValidationError as e:
        print(f"Validation error in {source_file}: {e}")
        return None


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    listings = []

    for filename in sorted(os.listdir(RAW_DIR)):
        path = os.path.join(RAW_DIR, filename)
        cars = load_car_blocks(path)

        for block in cars:
            flat = flatten_car(block)
            validated = extract_and_validate(flat, filename)
            if validated:
                listings.append(validated)

    seen = set()
    unique_listings = []
    for item in listings:
        if item.listing_id not in seen:
            seen.add(item.listing_id)
            unique_listings.append(item)

    print(f"parsed: {len(listings)}, after dedup: {len(unique_listings)}")

    rows = [item.model_dump() for item in unique_listings]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"saved {len(rows)} rows to {OUTPUT_FILE}")