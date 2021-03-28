# recipe_search

TTDS group project, search engine for recipes.

The project is set up for Python 3.8.2 and Django 3.1.4.
When running with Docker, the database used is PostgreSQL 13.1, along with Memcached and Nginx for caching and serving static files, respectively.

## Run with Docker

### Initializing Docker

- To start a daemon: `docker-compose up -d --build`
- Get output from daemon: `docker-compose logs -f` (adding `-t` shows timestamps)
- Start interactively: `docker-compose up --build`
- Create a superuser: `./cmd.sh manage createsuperuser`

### Stopping docker

- To kill it: `docker-compose down` (also removes containers but preserves state)
- Just suspend/stop it: `docker-compose stop`
- And then start it again: `docker-compose start`

### Other

- Check status of all images: `docker-compose ps`
- Whenever you make a change to the DB model, keep Docker running and run `./cmd.sh prepare` to create migrations
- If you're using tmux, `./cmd.sh tmux` will open up a new session with git, server (running in Docker), and a Django shell as windows. (must run from outside of a tmux shell)

Don't worry about constantly restarting Docker, it shouldn't be necessary. When Django notices a change in a Python file, it restarts itself, and when you change a template, it doesn't even need to restart because these are compiled every time when `DEBUG=True`

## Get up and running **without Docker** (not recommended)

1. `pip install pipenv`
2. Create a file called `.env` with the following contents:

```
PYTHONPATH=project

DJANGO_SETTINGS_MODULE=project.env

SECRET_KEY="Generate with https://djecrety.ir/"

DEBUG="True"
ALLOWED_HOSTS="127.0.0.1 0.0.0.0 localhost"
```

4. `pipenv run python project/manage.py migrate`
5. `pipenv run python project/manage.py createsuperuser`
6. `pipenv run python project/manage.py runserver 0.0.0.0:8000`
7. Open [0.0.0.0:8000](0.0.0.0:8000) or [localhost:8000](localhost:8000)

### Starting a server after that

- With Docker, you use `docker-compose up -d --build` or if containers have been created already `docker-compose start`
- Without Docker, it's `pipenv run python project/manage.py runserver 0.0.0.0:8000`
  - **But**, you should also migrate any new migrations and run `pipenv install` in case there were new changes. It's generally simpler to just use Docker.

## Database backup

### Dumping the database

1. Dump the DB within the container: `docker-compose exec db pg_dump -d recipesearch -U recipesearch_user -Fc -f pgdump.dump`
2. Copy it over from the container `docker cp recipe_search_db_1:/pgdump.dump ./`
3. _(optional)_ Delete the dump within the container: `docker-compose exec db rm pgdump.dump`

### Restoring the database

1. Copy dump over to the container: `docker cp pgdump.dump recipe_search_db_1:/`
2. Restore it in the container: `docker-compose exec db pg_restore -d recipesearch -U recipesearch_user pgdump.dump --clean`
   - The `--clean` tag overwrites previous DB data
3. _(optional)_ Delete the dump within the container: `docker-compose exec db rm pgdump.dump`
