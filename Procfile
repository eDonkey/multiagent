release: alembic upgrade head
web: gunicorn -k uvicorn.workers.UvicornWorker app.main:app
worker: celery -A app.worker.celery_app worker --loglevel=info
