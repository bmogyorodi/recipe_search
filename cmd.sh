#!/bin/bash

## To activate the pipenv virtualenv instead of spawning a shell
# . $(pipenv --venv)/bin/activate

# Prepare for a push (OUTSIDE Docker)
if [ "$1" = "prepare" ]; then
    docker-compose exec web pipenv install
    docker-compose exec web pipenv run python project/manage.py makemigrations
    docker-compose exec web pipenv run python project/manage.py makemessages -a
# Build (INSIDE Docker)
elif [[ "$1" = "build" ]]; then
    pipenv install
    pipenv run python project/manage.py collectstatic --noinput
    pipenv run python project/manage.py compilemessages
    pipenv run python project/manage.py migrate
# Run (INSIDE Docker)
elif [[ "$1" = "run" ]]; then
    ./cmd.sh build
    pipenv run gunicorn project.wsgi:application \
        --workers 2 \
        --bind 0.0.0.0:8000 \
        --reload \
        --log-level=debug
# Test project (OUTSIDE Docker)
elif [[ "$1" = "test" ]]; then
    if [ -n "$2" ]; then
        ./cmd.sh manage test $2
    else
        ./cmd.sh manage test project
    fi
# Use Docker's manage.py (OUTSIDE Docker)
elif [[ "$1" = "manage" ]]; then
    docker-compose exec web pipenv run python project/manage.py ${@:2}
# Create a TMUX session (OUTSIDE Docker)
elif [[ "$1" = "tmux" ]]; then
    SESSION="ttds"
    BASE_DIR="$(pwd)/"

    tmux new-session -d -s $SESSION
    tmux rename-window -t $SESSION:0 'git'
    tmux send-keys "gil" C-m
    tmux send-keys "q"
    tmux send-keys "gs" C-m

    # Setup server window
    tmux new-window -t $SESSION:1 -n 'SERVER' -c "${BASE_DIR}"
    tmux send-keys "docker-compose up -d --build" C-m
    tmux send-keys "docker-compose logs -f" C-m

    # Setup shell window
    tmux new-window -t $SESSION:2 -n 'SHELL' -c "${BASE_DIR}"
    tmux send-keys "./cmd.sh manage shell"

    # Set default window
    tmux select-window -t $SESSION:0

    # Attach to session
    # $TMUX isn't empty, so already running in TMUX
    if [ -n "$TMUX" ]; then
        echo "tmux already running"
    else
        tmux attach-session -t $SESSION
    fi
# Start services (SERVER)
elif [[ "$1" = "start" ]]; then
    # Probably run cmd.sh prepare first
    echo "Not implemented yet"
# Stop services (SERVER)
elif [[ "$1" = "stop" ]]; then
    echo "Not implemented yet"
# Reload services (SERVER)
elif [[ "$1" = "reload" ]]; then
    echo "Not implemented yet"
# Reload services (SERVER)
elif [[ "$1" = "restart" ]]; then
    echo "Not implemented yet"
# Bad command
else
    echo "Command '$1' not recognized"
fi
