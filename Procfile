web: cd src && gunicorn --timeout 180 app:app
worker: cd src && celery -A app.celery worker --loglevel=info