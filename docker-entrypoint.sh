#!/bin/sh
exec /usr/bin/tini -s -e 143 -- "$PYTHON_PATH"/gunicorn --bind=0.0.0.0:8000 "--log-level=$LOG_LEVEL" "--pythonpath=$PYTHON_PATH" "--workers=$WORKERS" "--timeout=$TIMEOUT" "--worker-class=$WORKER_CLASS" --worker-tmp-dir=/dev/shm "$@" serve:app
