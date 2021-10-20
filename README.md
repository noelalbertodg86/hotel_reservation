# hotel_reservation

## Stack
- Python 3.8
- FastAPI
- Uvicorn
- SqlAlchemy
- SQLite
- Alembic


## Running App
- Creating database
```shell script
make db
```
or

```shell script
pipenv run makemigrations
pipenv run migrate
```

- Populate db with initial data. (Hotel, Room and Reservations Rules )

```shell script
pipenv run seed
```

- Starting App
```shell script
make start
```
or
```shell script
pipenv run start
```

- Running tests
```shell script
make test
make unit-test
make int-test
```
or
```shell script
pipenv run pipenv run pytest tests/unit
pipenv run pytest tests/integration
```

# Description
The app was made using an layer architecture(Controllers, Services, Models).

## Endpoints documentation
Endpoints documentation and schemas are generated in swagger taking advantage of this FastAPI feature.
Once the App is running you can open ``{server:port}/docs`` url.

[local swagger url](http://0.0.0.0:8080/docs)

## Database model
![alt text](hotel_reservation_data_model.png)


