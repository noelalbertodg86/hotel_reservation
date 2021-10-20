FROM python:3.8.8-slim-buster AS app

RUN python -m pip install --upgrade pip
RUN python -m pip install pipenv

COPY ./ /app/
WORKDIR /app

RUN pipenv sync


FROM app as hotel_reservation

CMD ["./entrypoint.sh"]
