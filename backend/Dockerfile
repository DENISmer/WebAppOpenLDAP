FROM python:3.8.15-slim

ENV PYDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PATH=/usr/src/app/backend/venv/bin:$PATH

EXPOSE 8000

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

RUN mkdir backend

COPY ../backend/requirements.txt backend/.

COPY ../backend/api/ backend/api
COPY ../backend/startapp_server.sh startapp_server.sh

RUN python -m venv backend/venv
RUN python -m pip install -U pip
RUN python -m pip install -r backend/requirements.txt

RUN chmod u+x startapp_server.sh

CMD sh ./startapp_server.sh