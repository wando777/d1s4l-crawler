from flask import Blueprint, render_template, request, jsonify
from scraping.scraping_bot import ScrapingBot
from analytics.processador.grupo_cotas_processador import GruposCotasProcessor

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/scrape', methods=['POST'])
def scrape():
    username = request.form.get('username')
    password = request.form.get('password')
    sorteio = int(request.form.get('sorteio'))
    
    bot = ScrapingBot(headless=False)
    try:
        bot.login_to_site(username, password)
        bot.navigate_to_data_page()
        grupo_cotas = bot._get_grupo_cotas()
        processor = GruposCotasProcessor(grupo_cotas)
        result = processor.find_closest_cotas(sorteio)
        # processor.save_closest_cotas_to_csv(sorteio, 'sorteio.csv')
        
        return jsonify({
            'status': 'success',
            'grupos_cotas': grupo_cotas,
            'result': result
        })
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        bot.close()