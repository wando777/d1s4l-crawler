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
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-browser-side-navigation")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")

        environment = os.getenv('ENVIRONMENT', 'local')
        if environment == 'production':
            chrome_service = Service('/usr/local/bin/chromedriver')
            return webdriver.Chrome(service=chrome_service, options=chrome_options)
        else:
            return webdriver.Chrome(options=chrome_options)        
