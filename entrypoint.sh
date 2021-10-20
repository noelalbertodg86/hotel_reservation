#!/bin/bash

export PYTHONPATH=. ;\
rm hotel_reservation.db; \
rm migrations/versions/* ; \
pipenv run makemigrations ; \
pipenv run migrate; \
pipenv run seed; \
pipenv run start