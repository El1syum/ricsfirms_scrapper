import json

import requests

from config import config_params, config_cookies, config_headers


class Scrapper:
    def __init__(self, url: str, params: dict, headers=None, cookies=None):
        self.url = url
        self.params = params
        self.headers = headers if headers is not None else dict()
        self.cookies = cookies if cookies is not None else dict()

    def get_json(self):
        response = requests.get(
            self.url,
            params=self.params,
            cookies=self.cookies,
            headers=self.headers,
        )
        return response.json()

    def get_page_count(self, json_data):
        return json_data.get('pageCount')

    def main(self):
        json_data = self.get_json()
        page_count = self.get_page_count(json_data)
        print(page_count)


if __name__ == '__main__':
    scrapper = Scrapper(
        'https://www.ricsfirms.com/umbraco/api/surveyorSearchApi/results',
        params=config_params,
        cookies=config_cookies,
        headers=config_headers
    )
    scrapper.main()
