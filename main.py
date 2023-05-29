from config import config_params
from scraper import Scrapper


def main():
    scrapper = Scrapper(
        'https://www.ricsfirms.com/umbraco/api/surveyorSearchApi/results',
        params=config_params,
    )
    scrapper.main()


if __name__ == '__main__':
    main()
