# src/scraping/scraping_bot.py
from scraping.pages.login_page import LoginPage
from scraping.pages.data_page import DataPage
from scraping.utils.web_driver_factory import WebDriverFactory


class ScrapingBot:
    def __init__(self, headless=False):
        self.driver = WebDriverFactory.create_driver(headless)
        self.login_page = LoginPage(self.driver)
        self.data_page = DataPage(self.driver)

    def login_to_site(self, username, password):
        self.login_page.login(username, password)

    def navigate_to_data_page(self):
        self.data_page.navigate_to_data_page()

    def select_options(self, slider_value):
        self.data_page._select_options(slider_value)
    
    def click_on_grupo_links(self):
        self.data_page.click_on_grupo_links()

    def get_grupo_cotas(self):
        return self.data_page.grupo_cotas

    def close(self):
        self.driver.quit()
