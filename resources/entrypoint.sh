#!/usr/bin/env bash

set -e

touch -a /sunportal/log/uwsgi.log
touch -a /sunportal/log/flask.log

cd /sunportal/src/website

chown --recursive www-data:www-data /sunportal/

echo "Starting uwsgi server."
uwsgi --chdir=/sunportal/src/website \
    --module=wsgi:app \
    --master --pidfile=/tmp/project-master.pid \
    --socket=:8000 \
    --processes=5 \
    --uid=www-data --gid=www-data \
    --harakiri=20 \
    --post-buffering=16384 \
    --max-requests=5000 \
    --thunder-lock \
    --vacuum \
    --logfile-chown \
    --logto2=/sunportal/log/uwsgi.log \
    --ignore-sigpipe \
    --ignore-write-errors \
    --disable-write-exception
