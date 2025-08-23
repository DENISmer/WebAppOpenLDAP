#!/bin/bash

celery -A api.celery_app.app:celery_app worker --beat --concurrency=6 --loglevel=debug