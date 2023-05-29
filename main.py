from config import config_params, config_cookies, config_headers
from scraper import Scrapper


def main():
    scrapper = Scrapper(
        'https://www.ricsfirms.com/umbraco/api/surveyorSearchApi/results',
        params=config_params,
        cookies=config_cookies,
        headers=config_headers
    )
    scrapper.main()


if __name__ == '__main__':
    main()