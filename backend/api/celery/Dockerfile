FROM python:3.8.15-slim

ENV PYDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PATH=/usr/src/app/backend/venv/bin:$PATH

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

RUN mkdir backend

COPY ../../../backend/requirements.txt backend/.
COPY ../../../backend/api backend/api
COPY ../../../backend/__init__.py backend/__init__.py

RUN mv backend/api/celery/startapp_celery.sh .

RUN python -m venv backend/venv
RUN python -m pip install -r backend/requirements.txt

RUN chmod u+x startapp_celery.sh

CMD sh ./startapp_celery.sh