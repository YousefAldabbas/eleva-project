install:
	pip install poetry && \
	poetry install

run:
	docker-compose build && \
	docker-compose up

build:
	docker-compose build

up:
	docker-compose up

test:
	pytest -vx

start/mongo:
	docker run -d -p 27017:27017 mongo

start/redis:
	docker run -d -p 6379:6379 redis

start/local:
	uvicorn app.main:app --reload