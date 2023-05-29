import csv

import requests
from bs4 import BeautifulSoup


class Scrapper:
    TABLE_HEADERS = [
        'Title', 'Email', 'Phone', 'Address', 'Website', 'Welcome message', 'About', 'Services & Staff',
        'Business type', 'RICS Regulated', 'Residential', 'Commercial'
    ]

    def __init__(self, url: str, params: dict, headers=None, cookies=None, table_name='data.csv', max_page=None):
        self.url = url
        self.params = params
        self.headers = headers if headers is not None else dict()
        self.cookies = cookies if cookies is not None else dict()
        self.max_page = max_page
        self.table_name = table_name
        self.data = []
        self.create_csv()

    def create_csv(self):
        with open(self.table_name, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(self.TABLE_HEADERS)

    def save_to_csv(self, data):
        with open(self.table_name, 'a', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(data)

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

    def get_companies(self, json_data):
        return json_data.get('resultOffices')

    def get_company_page(self, company_id):
        company_url = f'https://www.ricsfirms.com/office/{company_id}'
        response = requests.get(
            company_url,
            headers=self.headers,
            cookies=self.cookies
        )
        return response.text

    def scrap_company_page(self, company_html):
        soup = BeautifulSoup(company_html, 'lxml')
        services = soup.find('div', id='tab-content-3').find_all('li')
        services = ', '.join(list(map(lambda i: i.text.strip(), services)))
        business_type = soup.find('div', id='tab-content-3') \
            .find('div', class_='showcase-section__content').text.strip()
        welcome_msg = soup.find('div', id='tab-content-1').find('p').text.strip()
        about = soup.find('div', id='tab-content-2').find('p', class_='office__about').text.strip()

        return [welcome_msg, about, services, business_type]

    def scrap_companies(self, companies):
        for company in companies:
            company_id = company.get('officeNumber')
            company_page = self.get_company_page(company_id)

            firm_name = company.get('firmName')
            firm_email = company.get('email')
            website = company.get('websiteUrl')
            telephone = company.get('telephone')
            address = company.get('address')
            regulated = 'Yes' if company.get('ricsRegulated') else 'No'
            commercial = 'Yes' if company.get('targetCommercial') else 'No'
            residential = 'Yes' if company.get('targetResidential') else 'No'
            welcome_msg, about, services, business_type = self.scrap_company_page(company_page)
            not_sorted_data = [firm_name, firm_email, telephone, address, website, welcome_msg, about, services,
                               business_type, regulated, commercial, residential]
            data = list(map(lambda i: i.replace(';', ',').strip(), not_sorted_data))
            self.data.append(data)

    def main(self):
        json_data = self.get_json()
        page_count = self.get_page_count(json_data)
        self.max_page = self.max_page + 1 if self.max_page else page_count + 1
        for page in range(1, self.max_page):
            self.params['page'] = page
            current_json_data = self.get_json()
            companies = self.get_companies(current_json_data)
            self.scrap_companies(companies)

        self.save_to_csv(self.data)


if __name__ == '__main__':
    ...
