from flask import Blueprint, render_template, request, jsonify
from analytics.processador.grupo_cotas_processador import GruposCotasProcessor
from scraping.scraping_bot import ScrapingBot

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    return render_template("index.html")


@main_blueprint.route("/scrape", methods=["POST"])
def scrape():
    username = request.form.get("username")
    password = request.form.get("password")
    sorteio = int(request.form.get("sorteio"))

    bot = ScrapingBot(headless=True)
    start_time = time.time()
    try:
        bot.login_to_site(username, password)
        print("Logged in successfully")
        bot.navigate_to_data_page()
        print("end scraping")
        grupo_cotas = bot.get_grupo_cotas()
        processor = GruposCotasProcessor(grupo_cotas)
        result = processor.find_closest_cotas(sorteio)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Scraping duration: {duration:.2f} seconds")

        return jsonify(
            {"status": "success", "grupos_cotas": grupo_cotas, "result": result}
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
import time
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        bot.close()
