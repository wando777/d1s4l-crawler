# src/scraping/scraping_bot.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep


class ScrapingBot:
    def __init__(self):
        # Inicializa o driver no construtor da classe
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Rodar o Chrome em modo "headless"
        self.driver = webdriver.Chrome(options=chrome_options)

    def login_to_site(self, username, password):
        # Abrir a página de login
        self.driver.get("https://www.disal360.com.br/Acesso/Entrar")

        # Preencher os campos de login
        self.driver.find_element(By.ID, "CPF").send_keys(username)
        self.driver.find_element(By.ID, "Senha").send_keys(password)

        # Enviar o formulário de login
        self.driver.find_element(By.ID, "btn-entrar").click()

        # Aguarda o carregamento da página
        sleep(3)

    def navigate_to_data_page(self):
        self.driver.get("https://www.disal360.com.br/Venda")
        sleep(2)

        # Encontrar o elemento com a classe 'main'
        main_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main"))
        )

        # Dentro do elemento 'main', encontrar a 'div' com a classe 'tipo_contrato'
        tipo_contrato_element = main_element.find_element(
            By.CLASS_NAME, "tipo_contrato"
        )

        andamento_button = main_element.find_element(
            By.XPATH, "//a[contains(., 'Grupos') and contains(., 'Andamento')]"
        )
        andamento_button.click()

        ## Clica no botão "Por parcelas"
        por_parcela_button = main_element.find_element(
            By.XPATH,
            "//input[@value='parcela']/following-sibling::div[contains(text(), 'Por Parcela')]",
        )
        por_parcela_button.click()

        ## Ajusta o valor da parcela para 2000
        self.set_slider_value(2000)

        ## Seleciona o primeiro plano da lista
        self.select_first_valid_option()

        ## marca a check box #divPasso1 > div > div:nth-child(2) > div > div:nth-child(4) > div > input[type=checkbox]
        check_box = main_element.find_element(
            By.CSS_SELECTOR,
            "#divPasso1 > div > div:nth-child(2) > div > div:nth-child(4) > div > input[type=checkbox]",
        )
        check_box.click()

        sleep(2)

        ## Seleciona o crédito
        self.select_first_credit_valid_option()

        ## Clica no botão "Buscar" //*[@id="divPasso1"]/div/div[2]/div/div[5]/div[3]/div/input
        buscar_button = main_element.find_element(
            By.XPATH, "//*[@id='divPasso1']/div/div[2]/div/div[5]/div[3]/div/input"
        )
        buscar_button.click()

        # slider = main_element.find_element(By.CSS_SELECTOR, 'input[type="range"].slider')
        # self.driver.execute_script("arguments[0].value = 2000;", slider)
        # self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", slider)
        # sleep(2)

        # # Clicar no botão "Andamento"
        # andamento_button = WebDriverWait(self.driver, 2).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, "ativo"))
        # )
        # andamento_button.click()

        # Aguarde o carregamento da página
        sleep(3)

    def set_slider_value(self, value):
        # Localizar o slider
        slider = self.driver.find_element(By.CSS_SELECTOR, 'input[type="range"].slider')
        slider_div = self.driver.find_element(By.CSS_SELECTOR, "div.main")

        # Obter a largura do slider
        slider_width = slider.size["width"]
        slider_div_width = slider_div.size["width"]

        # Obter o valor mínimo e máximo do slider
        min_value = int(slider.get_attribute("min"))
        max_value = int(slider.get_attribute("max"))

        # Calcular a porcentagem que o slider precisa ser movido para atingir o valor desejado
        # range_value = max_value - min_value
        # move_to_value = value - min_value

        # Verificar se o valor passado está dentro do intervalo permitido
        if value < min_value or value > max_value:
            raise ValueError(f"Valor fora do intervalo: {min_value} - {max_value}")

        # Calcular a proporção de deslocamento necessário (de 0 a 1)
        proportion = (value - min_value) / (max_value - min_value)

        # Calcular a quantidade de pixels para mover o slider
        move_by_pixels = proportion * slider_width * (slider_width / slider_div_width)
        # move_by_pixels = - (move_by_pixels - (move_by_pixels * 0.455))  # Ajuste fino

        # Simular o movimento do slider
        actions = ActionChains(self.driver)

        # Primeiro, movemos o slider até o início (posição 0)
        # actions.click_and_hold(slider).move_by_offset(-slider_width / 2, 0).release().perform()

        # Depois, movemos o slider pela quantidade de pixels calculada
        actions.click_and_hold(slider).move_by_offset(
            move_by_pixels, 0
        ).release().perform()

        sleep(2)

    def select_first_valid_option(self):
        # Localizar o dropdown pelo ID
        dropdown = self.driver.find_element(By.ID, "busca_andamento_plano")

        # Inicializar o objeto Select para interagir com o dropdown
        select = Select(dropdown)

        # Selecionar a primeira opção válida (índice 1, pois índice 0 é "Selecione")
        select.select_by_index(1)

        sleep(2)

    def select_first_credit_valid_option(self):
        # Localizar o dropdown pelo ID
        dropdown = self.driver.find_element(By.ID, "busca_andamento_modelo")

        # Inicializar o objeto Select para interagir com o dropdown
        select = Select(dropdown)

        # Selecionar a primeira opção válida (índice 1, pois índice 0 é "Selecione")
        select.select_by_index(1)

        sleep(2)

    def set_slider_value_loop(self, desired_value):
        # Localizar o slider
        slider = self.driver.find_element(By.CSS_SELECTOR, 'input[type="range"].slider')

        # Obter o valor mínimo e máximo do slider
        min_value = int(slider.get_attribute("min"))
        max_value = int(slider.get_attribute("max"))

        # Verificar se o valor passado está dentro do intervalo permitido
        if desired_value < min_value or desired_value > max_value:
            raise ValueError(f"Valor fora do intervalo: {min_value} - {max_value}")

        # Obter o valor atual do slider
        current_value = int(slider.get_attribute("value"))

        # Inicializar o ActionChains
        actions = ActionChains(self.driver)

        # Simular pequenos movimentos no slider até atingir o valor desejado
        while current_value != desired_value:
            move_by = (
                1 if current_value < desired_value else -1
            )  # Incrementar ou decrementar
            actions.click_and_hold(slider).move_by_offset(
                move_by, 0
            ).release().perform()
            sleep(0.05)  # Pequena espera para garantir a movimentação gradual
            current_value = int(
                slider.get_attribute("value")
            )  # Atualizar o valor atual do slider
            print(f"Slider atual: {current_value}")

        print(f"Slider ajustado para: {desired_value}")
        sleep(2)  # Aguarda o processamento do JavaScript, se necessário

    def close(self):
        # Fechar o navegador
        self.driver.quit()