build:
	docker-compose build

test:
	docker-compose up --build tests

migrations:
	 docker-compose run web ./manage.py makemigrations

migrate:
	 docker-compose run web ./manage.py migrate

celery:
	docker-compose up celery

server:
	docker-compose up web

superuser:
	docker-compose run web ./manage.py createsuperuser






