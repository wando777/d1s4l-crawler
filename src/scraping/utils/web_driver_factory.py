# src/scraping/utils/web_driver_factory.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriverFactory:
    @staticmethod
    def create_driver(headless=False):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        return webdriver.Chrome(options=chrome_options)
