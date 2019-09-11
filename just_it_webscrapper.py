from bs4 import BeautifulSoup
from selenium import webdriver
from requests import get, RequestException
from contextlib import closing
import pandas as pd
import urllib.request


class JustItWebscrapper():
    def __init__(self):
        self.base_url = 'https://justjoin.it'

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

    def get_offers(self, city='all', name='javascript', exp_lvl='all', salary=''):
        url = f'{self.base_url}/{city}/{name}/{exp_lvl}/{salary}'
        raw_html = self.get_page_content(url)
        zupa = BeautifulSoup(raw_html, 'html.parser')
        zupa = zupa.find_all('href')
        return str(zupa)

    def log_error(selfe, error):
        print(error)
