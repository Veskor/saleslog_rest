## Docs
  Brief list of commands to have when working with backend

# Running
  docker-compose build
  docker-compose up

# Loading data
  docker-compose run web python manage.py runscript lib/load_fixtures.py

# Dump data
  docker-compose run web python manage.py runscript lib/dump_fixtures.py

# Testing
  docker-compose run web python manage.py test
