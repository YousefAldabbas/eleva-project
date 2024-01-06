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