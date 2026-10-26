import json
import time
from datetime import datetime, timezone

import requests

BRANDS = ["toyota", "honda", "mazda"]
PAGES = 8

WAIT_REQUEST = 10
WAIT_BETWEEN_REQUESTS = 5

manifest = {}

session = requests.Session()
for brand in BRANDS:
    for page in range(1, PAGES + 1):
        urls = f"https://auto.drom.ru/{brand}/all/page{page}/"
    
        try:
            response = session.get(urls, timeout=WAIT_REQUEST)
            response.raise_for_status()
            
            filename = f"{brand}_page_{page}.html"
            with open(f"data/raw/{filename}", "wb") as f:
                f.write(response.content)

            manifest[filename] = datetime.now(timezone.utc).isoformat(timespec="seconds")

            print(response.status_code)
            print(len(response.content))
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        time.sleep(WAIT_BETWEEN_REQUESTS)

with open("data/manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)
print(f"manifest: {len(manifest)} files")