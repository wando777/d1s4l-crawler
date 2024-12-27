# src/scraping/utils/web_driver_factory.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os


class WebDriverFactory:
    @staticmethod
    def create_driver(headless=False):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--remote-debugging-port=9222")

        environment = os.getenv("ENVIRONMENT", "local")
        if environment == "local":
            return webdriver.Chrome(options=chrome_options)
        else:
            chrome_options.binary_location = os.environ.get(
                "GOOGLE_CHROME_BIN", "/app/.chrome-for-testing/chrome-linux64/chrome"
            )
            chrome_driver_path = os.environ.get(
                "CHROMEDRIVER_PATH", "/app/.chrome-for-testing/chromedriver-linux64/chromedriver"
            )
            service = Service(chrome_driver_path)
            return webdriver.Chrome(service=service, options=chrome_options)
