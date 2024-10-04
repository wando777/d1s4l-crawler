from scraping.scraping_bot import ScrapingBot

# Configurações
USERNAME = "02368152377"
PASSWORD = "123456"
HEADLESS = False


def initialize_bot(headless):
    """Inicializa o bot de scraping."""
    return ScrapingBot(headless=headless)


def perform_login(bot, username, password):
    """Realiza o login no site."""
    bot.login_to_site(username, password)


def navigate_and_extract_data(bot):
    """Navega para a página de dados e realiza a extração."""
    bot.navigate_to_data_page()


def main():
    """Função principal para executar o scraping."""
    bot = None
    try:
        # Inicializar o bot de scraping
        bot = initialize_bot(HEADLESS)

        # Fazer login
        perform_login(bot, USERNAME, PASSWORD)

        # Navegar para a página de dados e extrair informações
        navigate_and_extract_data(bot)

    # except Exception as e:
    #     if e == TimeoutError:
    #         print("O sistema da Disal está lento, favor tentar novamente mais tarde.")
    #     print(f"Ocorreu um erro: {e}")
    finally:
        if bot:
            bot.close()


if __name__ == "__main__":
    main()
