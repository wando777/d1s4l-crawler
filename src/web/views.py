from flask import Blueprint, render_template, request, jsonify
from analytics.processador.grupo_cotas_processador import GruposCotasProcessor
from scraping.scraping_bot import ScrapingBot
from data.scraping_model import ScrapingResult
from data.database import db
from app import celery
import random
import string
import logging
from sqlalchemy.exc import OperationalError
from celery.exceptions import MaxRetriesExceededError


main_blueprint = Blueprint("main", __name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

def generate_friendly_id(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

@main_blueprint.route("/")
def index():
    return render_template("index.html")

@main_blueprint.route("/scrape", methods=["POST"])
def scrape():
    username = request.form.get("username")
    password = request.form.get("password")
    sorteio = int(request.form.get("sorteio"))

    scrape_id = generate_friendly_id()
    scraping_result = ScrapingResult(id=scrape_id, status='pending')
    db.session.add(scraping_result)
    db.session.commit()

    scrape_task.delay(scrape_id, username, password, sorteio)

    return jsonify({"status": "success", "scrape_id": scrape_id})

@main_blueprint.route("/scrape/status/<scrape_id>", methods=["GET"])
def scrape_status(scrape_id):
    scraping_result = ScrapingResult.query.get(scrape_id)
    if not scraping_result:
        return jsonify({"status": "error", "message": "ID de busca não encontrado"})
    if scraping_result.status == 'pending':
        return jsonify({"status": "pending", "message": "Processando... Aguarde um momento"})
    elif scraping_result.status == 'completed':
        return jsonify({"status": "success", "grupos_cotas": scraping_result.result['grupos_cotas'], "result": scraping_result.result['result']})
    else:
        return jsonify({"status": "error", "message": "Ocorreu um erro durante o processamento, faça uma nova busca"})

@celery.task(bind=True, max_retries=3)
def scrape_task(self, scrape_id, username, password, sorteio):
    bot = ScrapingBot(headless=True)
    try:
        bot.login_to_site(username, password)
        logging.info(f"Logged in successfully with scrape_id: {scrape_id}")
        bot.navigate_to_data_page()
        logging.info(f"Navigated to data page with scrape_id: {scrape_id}")
        bot.select_options()
        logging.info(f"Options selected with scrape_id: {scrape_id}")
        bot.click_on_grupo_links()
        logging.info(f"Clicked on grupo links with scrape_id: {scrape_id}")
        grupo_cotas = bot.get_grupo_cotas()
        processor = GruposCotasProcessor(grupo_cotas)
        result = processor.find_closest_cotas(sorteio)

        with db.session.begin_nested():
            scraping_result = ScrapingResult.query.get(scrape_id)
            scraping_result.status = 'completed'
            scraping_result.result = {'grupos_cotas': grupo_cotas, 'result': result}
            db.session.commit()
    except OperationalError as e:
        logging.error(f"OperationalError occurred: {e}")
        try:
            self.retry(exc=e, countdown=5)
        except MaxRetriesExceededError:
            with db.session.begin_nested():
                scraping_result = ScrapingResult.query.get(scrape_id)
                scraping_result.status = 'failed'
                db.session.commit()
    except Exception as e:
        logging.error(f"An error occurred during scraping: {e}")
        with db.session.begin_nested():
            scraping_result = ScrapingResult.query.get(scrape_id)
            scraping_result.status = 'failed'
            db.session.commit()
        import traceback
        traceback.print_exc()
    finally:
        bot.close()
        db.session.remove()