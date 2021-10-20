db:
	rm hotel_reservation.db; \
	rm migrations/versions/* ; \
	pipenv run makemigrations ; \
	pipenv run migrate


start:
	./entrypoint.sh

unit-test:
	pipenv run pytest tests/unit

int-test: db
	pipenv run seed
	pipenv run pytest tests/integration

code-analysis:
	black . ;\
	flake8 ./hotel_reservation ;\
	flake8 ./tests

test: unit-test int-test

build-image:
	docker build . --tag "hotel_reservation"

start-w-docker: build-image
	docker run -p 8080:8080 hotel_reservation

