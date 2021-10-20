db:
	rm hotel_reservation.db; \
	rm migrations/versions/* ; \
	pipenv run makemigrations ; \
	pipenv run migrate


start: db
	pipenv run seed
	pipenv run start

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
