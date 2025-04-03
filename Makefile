install:
	poetry install

start:
	gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000

local:
	python manage.py runserver

lint:
	ruff check . --fix

test:
	python manage.py test
