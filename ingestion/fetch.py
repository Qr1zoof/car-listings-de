import time

import requests

WAIT_REQUEST = 10
WAIT_BETWEEN_REQUESTS = 5

test_url = ["https://auto.drom.ru/toyota/", "https://auto.drom.ru/honda/", "https://auto.drom.ru/mazda/"]



session = requests.Session()
for urls in test_url:
    try:
        response = session.get(urls, timeout=WAIT_REQUEST)
        response.raise_for_status()
        
        data_name = urls.split('/')[-2] 
        with open(f"data/raw/{data_name}.html", "wb") as f:
            f.write(response.content)
        print(response.status_code)
        print(len(response.content))
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    time.sleep(WAIT_BETWEEN_REQUESTS)