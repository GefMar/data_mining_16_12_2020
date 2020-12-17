import json
import time
from pathlib import Path
import requests


class StatusCodeError(Exception):
    def __init__(self, txt):
        self.txt = txt


class Parser5ka:
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0"}
    
    def __init__(self, start_url):
        self.start_url = start_url
    
    def run(self):
        try:
            for product in self.parse(self.start_url):
                file_path = Path(__file__).parent.joinpath('products', f'{product["id"]}.json')
                self.save(product, file_path)
        except requests.exceptions.MissingSchema:
            exit()
    
    def get_response(self, url, **kwargs):
        while True:
            try:
                response = requests.get(url, **kwargs)
                if response.status_code != 200:
                    raise StatusCodeError
                time.sleep(0.05)
                return response
            except (requests.exceptions.HTTPError,
                    StatusCodeError,
                    requests.exceptions.BaseHTTPError,
                    requests.exceptions.ConnectTimeout):
                time.sleep(0.25)
    
    def parse(self, url):
        while url:
            response = self.get_response(url, headers=self.headers)
            data = response.json()
            url = data['next']
            for product in data['results']:
                yield product
    
    def save(self, data: dict, file_path):
        with open(file_path, 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)


if __name__ == '__main__':
    parser = Parser5ka("djkhjdhjkdhdj")
    parser.run()
