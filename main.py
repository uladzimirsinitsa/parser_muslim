
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


def get_names_files(path: str) -> list:
    list_ = []
    for _, _, names in os.walk(path):
        list_.extend(iter(names))
    return list_


def save_data(path: str, dict_: dict, name: str) -> None:
    name = name.replace('/', '')
    with open(f'{path}/{name}.json', 'w', encoding='utf-8') as file:
        json.dump(dict_, file, indent=4, ensure_ascii=False)


def main():
    service = Service(PATH_DRIVER)
    options = ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=service, options=options)


if __name__ == '__main__':
    main()
