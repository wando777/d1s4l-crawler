import sys
import os
from flask import Flask
from dotenv import load_dotenv
from data.database import db
from infra.celery_app import create_celery_app

# Adicionar o diretório 'src' ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web/templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web/static'))

# Definir a secret_key para a aplicação
app.secret_key = os.urandom(24)

# Configurar SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEMBO_DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_timeout': 30,
    'max_overflow': 10,
    'pool_size': 5,
}
db.init_app(app)
# Crie as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Configurar Celery
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
app.config.update(
    CELERY_BROKER_URL=redis_url,
    CELERY_RESULT_BACKEND=redis_url,
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERYD_CONCURRENCY=2,  # Limitar o número de workers
    CELERYD_PREFETCH_MULTIPLIER=1,  # Limitar o número de tarefas pré-buscadas
    CELERY_ACKS_LATE=True,  # Habilitar reconhecimento tardio
    CELERY_TASK_SOFT_TIME_LIMIT=300,  # Limite de tempo suave para tarefas
    CELERY_TASK_TIME_LIMIT=600,  # Limite de tempo rígido para tarefas
)

# Se estiver em produção, configurar SSL
if 'REDIS_URL' in os.environ:
    app.config.update(
        CELERY_BROKER_USE_SSL={
            'ssl_cert_reqs': 'CERT_NONE'
        },
        CELERY_REDIS_BACKEND_USE_SSL={
            'ssl_cert_reqs': 'CERT_NONE'
        }
    )

celery = create_celery_app(app)

from web.views import main_blueprint
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)