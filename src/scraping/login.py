from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

driver = None

def login_to_site(username, password):
    global driver

    # Configurar o WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Para rodar sem abrir o navegador
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get("https://www.disal360.com.br/Acesso/Entrar")  # Página de login

    # Localizar campos de login e senha e o botão de login
    username_field = driver.find_element(By.ID, "CPF")
    password_field = driver.find_element(By.ID, "Senha")
    login_button = driver.find_element(By.ID, "btn-entrar")

    # Inserir credenciais
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Enviar o formulário
    login_button.click()

    # Aguardar o carregamento da página
    time.sleep(3)