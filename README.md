# recipe_search
TTDS group project, search engine for recipes

The project is set up for Python 3.8.2 (or probably any Python 3.8) and Django 3.1.4.
The DB is currently set to be SQlite3 for its simplicity, and in production, we should set this to PostgreSQL.

### Get up and running
1. `pip install pipenv`
2. `pipenv install` in the folder with Pipfile
3. Create a file called `.env` with the following contents:

```
PYTHONPATH=project

DJANGO_SETTINGS_MODULE=project.env

SECRET_KEY="Generate with https://djecrety.ir/"

DEBUG="True"
ALLOWED_HOSTS="127.0.0.1 0.0.0.0 localhost"
```

4. `pipenv run python proejct/manage.py migrate`
5. `pipenv run python proejct/manage.py createsuperuser`
6. `pipenv run python project/manage.py runserver 0.0.0.0:8000`
7. Open up localhost:8000, 0.0.0.0:8000 or 127.0.0.1:8000
