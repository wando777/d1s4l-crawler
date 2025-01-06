from infra.celery_config import make_celery

def create_celery_app(app):
    celery = make_celery(app)
    return celery