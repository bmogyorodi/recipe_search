#!/bin/bash

## To activate the pipenv virtualenv instead of spawning a shell
# . $(pipenv --venv)/bin/activate

# Prepare for a push (CLIENT)
if [ "$1" = "prepare" ]; then
    pipenv install
    pipenv run python project/manage.py makemigrations
    pipenv run python project/manage.py makemessages -a
# Build (CLIENT + SERVER)
elif [[ "$1" = "build" ]]; then
    pipenv install
    pipenv run python project/manage.py collectstatic --noinput
    pipenv run python project/manage.py compilemessages
    pipenv run python project/manage.py migrate
# Run (CLIENT + SERVER)
elif [[ "$1" = "run" ]]; then
    ./cmd.sh build
    pipenv run python project/manage.py runserver 0.0.0.0:8000
# Test project (CLIENT)
elif [[ "$1" = "test" ]]; then
    if [ -n "$2" ]; then
        pipenv run python project/manage.py test $2
    else
        pipenv run python project/manage.py test project
    fi
# Create a TMUX session (CLIENT)
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
    tmux send-keys "./cmd.sh run" C-m

    # Setup shell window
    tmux new-window -t $SESSION:2 -n 'SHELL' -c "${BASE_DIR}project"
    tmux send-keys "pipenv run python manage.py shell" C-m

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
