from scraping.login import login_to_site
from scraping.navigation import navigate_to_data_page
from scraping.scrapingbot import ScrapingBot

# from scraping.extract_data import extract_table_data, process_table_datas


def main():
    # Inicializar o bot de scraping
    bot = ScrapingBot()

    # Credenciais
    username = "02368152377"
    password = "123456"

    # Fazer login
    bot.login_to_site(username, password)

    # Navegar para a página de dados
    bot.navigate_to_data_page()


if __name__ == "__main__":
    main()
    # Extração dos dados da tabela
    # data = extract_table_data()

    # # Processamento dos dados
    # processed_data = process_table_data(data)

    # print(processed_data)
