install:
	poetry install

start:
	gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000
