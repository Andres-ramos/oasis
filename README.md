# oasis
Applicacion de impacto social

Create a .env file from example.env

To run the project run `docker-compose up -d` in root directory to create the database

Run `python manage.py migrate` to create database tables

Run `python manage.py runserver` to actually run the django application


For NDVI task:

Run `python manage.py runscript ndvi` in order to insert ndvi raster into database

Run `python manage.py runscript ndvi_logic` in order to test ndvi overlap logic

