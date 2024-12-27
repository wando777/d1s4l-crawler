from flask import Blueprint, render_template, request, jsonify, session
from analytics.processador.grupo_cotas_processador import GruposCotasProcessor
from scraping.scraping_bot import ScrapingBot
import uuid

main_blueprint = Blueprint("main", __name__)

# Armazenamento temporário para instâncias do ScrapingBot
bot_storage = {}

@main_blueprint.route("/")
def index():
    return render_template("index.html")

@main_blueprint.route("/scrape/login", methods=["POST"])
def scrape_login():
    username = request.form.get("username")
    password = request.form.get("password")

    bot = ScrapingBot(headless=True)
    bot_id = str(uuid.uuid4())
    bot_storage[bot_id] = bot
    session['bot_id'] = bot_id

    try:
        bot.login_to_site(username, password)
        print("Logged in successfully")
        return jsonify({"status": "success", "message": "Logged in successfully"})
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)})

@main_blueprint.route("/scrape/navigate", methods=["POST"])
def scrape_navigate():
    bot_id = session.get('bot_id')
    if not bot_id or bot_id not in bot_storage:
        return jsonify({"status": "error", "message": "Bot not found in session"})

    bot = bot_storage[bot_id]
    try:
        bot.navigate_to_data_page()
        print("Navigated to data page")
        return jsonify({"status": "success", "message": "Navigated to data page"})
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)})

@main_blueprint.route("/scrape/select_options", methods=["POST"])
def scrape_select_options():
    bot_id = session.get('bot_id')
    if not bot_id or bot_id not in bot_storage:
        return jsonify({"status": "error", "message": "Bot not found in session"})

    bot = bot_storage[bot_id]
    try:
        bot.select_options()
        print("Options selected")
        return jsonify({"status": "success", "message": "Options selected"})
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)})

@main_blueprint.route("/scrape/extract", methods=["POST"])
def scrape_extract():
    bot_id = session.get('bot_id')
    if not bot_id or bot_id not in bot_storage:
        return jsonify({"status": "error", "message": "Bot not found in session"})

    bot = bot_storage[bot_id]
    sorteio = int(request.form.get("sorteio"))

    try:
        grupo_cotas = bot.get_grupo_cotas()
        processor = GruposCotasProcessor(grupo_cotas)
        result = processor.find_closest_cotas(sorteio)
        print("Data extracted and processed")
        return jsonify({"status": "success", "grupos_cotas": grupo_cotas, "result": result})
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        bot.close()
        session.pop('bot_id', None)
        del bot_storage[bot_id]