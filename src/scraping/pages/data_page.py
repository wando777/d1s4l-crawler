import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from scraping.utils.html_writer import write_html

class DataPage:
    def __init__(self, driver):
        self.driver = driver
        self.grupo_cotas = {}

    def ensure_login_complete(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "home"))
        )

    def navigate_to_data_page(self):
        time.sleep(1)
        self.driver.get("https://www.disal360.com.br/Venda")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        main_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main"))
        )
        self._wait_loader()
        andamento_button = WebDriverWait(main_element, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='conteudo']/div[1]/a[2]"))
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", andamento_button
        )
        andamento_button.click()
        self._wait_loader()
        self._select_options(main_element)
        self._click_on_grupo_links(main_element)

    def _select_options(self, main_element):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "check"))
        )
        por_parcela_button = WebDriverWait(main_element, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[@value='parcela']/following-sibling::div[contains(text(), 'Por Parcela')]",
                )
            )
        )
        por_parcela_button.click()
        self._set_slider_value_js(2000)
        self._select_first_valid_option("busca_andamento_plano")
        check_box = WebDriverWait(main_element, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[4]/div/div[2]/div/div[2]/div/div[4]/div/input",
                )
            )
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", check_box)
        check_box.click()
        self._select_first_valid_option("busca_andamento_modelo")
        buscar_button = WebDriverWait(main_element, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[@id='divPasso1']/div/div[2]/div/div[5]/div[3]/div/input",
                )
            )
        )
        buscar_button.click()

    def _set_slider_value_js(self, value):
        slider = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[4]/div/div[2]/div/div[2]/div/div[1]/div/input",
                )
            )
        )
        min_value = int(slider.get_attribute("min"))
        max_value = int(slider.get_attribute("max"))
        if value < min_value or value > max_value:
            raise ValueError(f"Valor fora do intervalo: {min_value} - {max_value}")

        # Usar JavaScript para definir diretamente o valor do slider e disparar eventos
        script = """
        var slider = arguments[0];
        var value = arguments[1];
        slider.value = value;
        slider.dispatchEvent(new Event('input'));
        slider.dispatchEvent(new Event('change'));
        """
        self.driver.execute_script(script, slider, value)

        # Verificar o valor do slider para depuração
        current_value = self.driver.execute_script("return arguments[0].value;", slider)
        print(f"Current slider value: {current_value}")

    def _select_first_valid_option(self, element_id):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        select = Select(dropdown)
        WebDriverWait(self.driver, 10).until(lambda _: len(select.options) > 1)
        options = [option.text for option in select.options]
        print(f"Available options: {options}")
        select.select_by_index(1)

    def _click_on_grupo_links(self, main_element):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='divPasso21']/div/div/div/div/div/table")
            )
        )
        grupo_links = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/td[9]/a"))
        )
        for link in grupo_links:
            self._wait_loader()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(link))
            self.driver.execute_script("arguments[0].click();", link)
            self._wait_loader()
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(
                    (By.CLASS_NAME, "fancybox-overlay fancybox-overlay-fixed")
                )
            )
            self._extract_cotas()

    def _extract_cotas(self):
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(
                (By.CLASS_NAME, "fancybox-overlay fancybox-overlay-fixed")
            )
        )
        page_html = self.driver.page_source
        soup = BeautifulSoup(page_html, "html.parser")
        div_passo = soup.find("div", {"id": "divPasso22"})
        if div_passo:
            grupo_paragraph = div_passo.find("p")
            if grupo_paragraph:
                grupo_info = grupo_paragraph.get_text(strip=True)
                grupo_numero = (
                    grupo_info.split("Grupo:")[-1].split("Parcela:")[0].strip()
                )
                cotas = [
                    radio["value"]
                    for radio in div_passo.find_all("input", {"name": "cota"})
                ]
                self.grupo_cotas[grupo_numero] = cotas
                print(f"Grupo {grupo_numero}: Cotas extraídas -> {cotas}")

    def _wait_loader(self):
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "loader"))
        )