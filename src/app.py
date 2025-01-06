import sys
import os
from flask import Flask
from dotenv import load_dotenv

# Adicionar o diretório 'src' ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web.views import main_blueprint
from data.database import db

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'web/templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'web/static'))

# Definir a secret_key para a aplicação
app.secret_key = os.urandom(24)

# Configurar SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEMBO_DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)