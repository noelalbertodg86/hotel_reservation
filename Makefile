db-reset:
	rm sql_app.db; \
	rm migrations/versions/* ; \
	pipenv run makemigrations ; \
	pipenv run migrate


start: db-reset
	pipenv run seed
	pipenv run start

unit-test:
	pipenv run pytest tests/unit

int-test: db-reset
	pipenv run seed
	pipenv run pytest tests/integration