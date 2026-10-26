import time

import requests

BRANDS = ["toyota", "honda", "mazda"]
PAGES = 8

WAIT_REQUEST = 10
WAIT_BETWEEN_REQUESTS = 5

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
            print(response.status_code)
            print(len(response.content))
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        time.sleep(WAIT_BETWEEN_REQUESTS)