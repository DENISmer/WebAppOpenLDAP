#!/bin/bash

gunicorn --workers 6 --bind 0.0.0.0:8000 backend.api.app:app
