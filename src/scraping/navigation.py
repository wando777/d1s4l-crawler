from selenium.webdriver.common.by import By
import time

# Importa o driver como variável global
from .login import driver

def navigate_to_data_page():
    # Suponha que há um link no menu que nos leva para a página com as tabelas
    data_page_link = driver.find_element(By.LINK_TEXT, " Nova Venda ")
    data_page_link.click()
    time.sleep(3)
