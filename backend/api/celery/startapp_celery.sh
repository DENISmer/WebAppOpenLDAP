#!/bin/bash

celery -A backend.api.celery.celery_app:celery_app worker --beat --concurrency=6