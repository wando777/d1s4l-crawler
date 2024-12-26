from flask import Flask
from web.views import main_blueprint
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'web/templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'web/static'))
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
