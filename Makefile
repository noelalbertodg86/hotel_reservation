db-reset:
	rm sql_app.db; \
	rm migrations/versions/* ; \
	pipenv run makemigrations ; \
	pipenv run migrate
