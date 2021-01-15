# recipe_search

TTDS group project, search engine for recipes.

The project is set up for Python 3.8.2 and Django 3.1.4.
When running with Docker, the database used is PostgreSQL 13.1, along with Memcached and Nginx for caching and serving static files, respectively.

## Run with Docker

### Initializing Docker

- To start a daemon: `docker-compose up -d --build`
- Get output from daemon: `docker-compose logs -f` (adding `-t` shows timestamps)
- Start interactively: `docker-compose up --build`

### Stopping docker

- To kill it: `docker-compose down` (also removes containers but preserves state)
- Just suspend/stop it: `docker-compose stop`
- And then start it again: `docker-compose start`

### Other

- Check status of all images: `docker-compose ps`

Don't worry about constantly restarting Docker, it shouldn't be necessary. When Django notices a change in a Python file, it restarts itself, and when you change a template, it doesn't even need to restart because these are compiled every time when `DEBUG=True`

## Get up and running **without Docker**

1. `pip install pipenv`
2. Create a file called `.env` with the following contents:

```
PYTHONPATH=project

DJANGO_SETTINGS_MODULE=project.env

SECRET_KEY="Generate with https://djecrety.ir/"

DEBUG="True"
ALLOWED_HOSTS="127.0.0.1 0.0.0.0 localhost"
```

4. `./cmd.sh build`
5. `pipenv run python project/manage.py createsuperuser`
6. `./cmd.sh run`
7. Open [0.0.0.0:8000](0.0.0.0:8000)

### Starting a server after that

Just run `./cmd.sh run`
There are several more commands in the file I use regularly in other projects and a placeholder for when we'd deploy on a server.
If you're using tmux, `./cmd.sh tmux` will open up a new session with git, server, and shell as windows. (must run from outside of a tmux shell)
