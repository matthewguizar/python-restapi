#!/bin/sh

flask bd upgrade

exec gunicorn --bind 0.0.0.0:80 "app:create_app()"