
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
PATH_URLS = os.environ['PATH_URLS']
PATH_CARDS = os.environ['PATH_CARDS']


def get_urls(path: str) -> list:
    with open(path, encoding='utf-8') as file:
        return file.readlines()


def save_data(path: str, data, name: str) -> None:
    with open(f'{path}/{name}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    service = Service(PATH_DRIVER)
    options = ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=service, options=options)
    for count, url in enumerate(get_urls(PATH_URLS), start=0):
        time.sleep(4)
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        name = '-'.join(('sura', driver.current_url[39:].split('-')[1]))

        data = soup.find_all(class_='verse-item')
        list_ = []
        index = 0 if count == 0 else 1
        for item in data[index:]:
            surah = int(item.find(
                class_='verse-item-title'
                ).get_text(strip=True).partition(':')[0])
            ayat = int(item.find(
                class_='verse-item-title'
                ).get_text(strip=True).partition(':')[2])
            try:
                text = item.find(
                    class_='arab_podpis'
                    ).find('p').get_text(strip=True)
            except AttributeError:
                continue
            dict_ = {
                'surah': surah,
                'ayat': ayat,
                'text': text
            }
            list_.append(dict_)
        save_data(PATH_CARDS, list_, name)
    driver.quit()

if __name__ == '__main__':
    main()
