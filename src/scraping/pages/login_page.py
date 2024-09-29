# src/scraping/pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.get("https://www.disal360.com.br/Acesso/Entrar")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "CPF"))
        ).send_keys(username)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "Senha"))
        ).send_keys(password)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn-entrar"))
        ).click()
