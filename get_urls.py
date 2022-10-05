
import json
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


PATH_DRIVER = os.environ['PATH_DRIVER']
URL = os.environ['URL']
DOMAIN = os.environ['DOMAIN']


def main():
    service = Service(PATH_DRIVER)
    options = ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    data = soup.find_all(class_='list-unstyled list-koran-suras')
    a = []
    for item in data:
        list_ = item.find_all('a')
        a.extend(list_)
    urls = [''.join((DOMAIN, item.get('href'))) for item in a]
    with open('data/urls/urls.txt', 'w', encoding='utf-8') as file:
        for url in urls:
            file.write(''.join((url, '\n')))


if __name__ == '__main__':
    main()
