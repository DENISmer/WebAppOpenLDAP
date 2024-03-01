FROM python:3.8.15-slim

ENV PYDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PATH=/usr/src/app/backend/venv/bin:$PATH

RUN useradd -ms /bin/bash web-server-user

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

RUN mkdir backend files instance

COPY ../../../backend/requirements.txt backend/.
COPY ../../../backend/api backend/api
COPY ../../../backend/__init__.py backend/__init__.py

RUN mv backend/api/celery/startapp_celery.sh .

RUN python -m venv backend/venv
RUN python -m pip install -U pip
RUN python -m pip install -r backend/requirements.txt

RUN chmod u+x startapp_celery.sh

RUN chown -R web-server-user:web-server-user startapp_celery.sh files instance
RUN chmod ugo+w /usr/src/app/backend/ /usr/src/app/

USER web-server-user

CMD sh ./startapp_celery.sh