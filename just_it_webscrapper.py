from bs4 import BeautifulSoup
from selenium import webdriver
from requests import get, RequestException
from contextlib import closing
import pandas as pd
import urllib.request
import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class JustItWebscrapper():
    def __init__(self, os):
        self.base_url = 'https://justjoin.it'
        self.os = os  # TODO dac rozroznienie drivera
        self.just_driver = webdriver.Chrome(self.get_driver())
        self.wait = WebDriverWait(self.just_driver, 10)

    def get_offers(self, city='', name='', exp_lvl='', salary_range=''):
        if city != '':
            city = f'{city}/'
        if name != '':
            name = f'{name}/'
        if exp_lvl != '':
            exp_lvl = f'{exp_lvl}/'
        if salary_range != '':
            salary_range = f'{salary_range}/'

        xpath_base = '//*[@id="body-top"]/div[3]/div[2]/div/ui-view/offers-list/ul/li'
        url = f'{self.base_url}/{city}{name}{exp_lvl}{salary_range}'

        self.just_driver.get(url)
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="body-top"]/div[3]/div[2]/div/ui-view/offers-list/ul/li[1]')))
        offer_number = len(self.just_driver.find_elements_by_xpath(xpath_base))
        assert offer_number != 0
        single_offer = []
        offer_list = [[]]

        for i in range(1, offer_number):
            job_title_xpath = f'{xpath_base}[{i}]/offer-item/a/div[2]/div[1]/span'
            job_title = self.just_driver.find_element_by_xpath(job_title_xpath).text
            assert job_title != ''  # TODO funckja dla ogołu
            salary_xpath = f'{xpath_base}[{i}]/offer-item/a/div[2]/div[1]/div/span[1]/span'
            salary = self.just_driver.find_element_by_xpath(salary_xpath).text
            age_xpath = f'{xpath_base}[{i}]/offer-item/a/div[2]/div[1]/div/span[2]'
            age = self.just_driver.find_element_by_xpath(age_xpath).text
            company_xpath = f'{xpath_base}[{i}]/offer-item/a/div[2]/div[2]/span/span[1]'
            company = self.just_driver.find_element_by_xpath(company_xpath).text

            single_offer.append(job_title)
            single_offer.append(salary)
            single_offer.append(age)
            single_offer.append(company)

            offer_list.append(single_offer)
        pprint.pprint(offer_list)

    def check_offer_list(self, offer_list):
        assert offer_list is not None


    def get_page_content(self, url):
        try:
            with closing(get(url, stream=True)) as resp:
                if self.check_response(resp):
                    print(resp.content)
                    return resp.content
                else:
                    return None
        except RequestException as re:
            self.log_error(f'Error during requests to {url} : {str(re)}')

    def check_response(self, response):
        content_type = response.headers['Content-Type'].lower()
        return (response.status_code == 200 and content_type is not None and content_type.find('html') > -1)

    def get_driver(self):
        if self.os == 'windows':
            driver_path = r'./drivers/chromedriver_win.exe'
        elif self.os == 'linux':
            driver_path = r'./drivers/chromedriver_linux'
        elif self.os == 'macos':
            driver_path = r'./drivers/chromedriver_mac'
        else:
            raise SystemError('Nie rozpoznano systemu!')
        return driver_path

    def log_error(selfe, error):
        print(error)
