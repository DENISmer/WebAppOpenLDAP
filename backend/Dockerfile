FROM python:3.8.15-slim

ENV PYDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PATH=/usr/src/app/backend/venv/bin:$PATH

#EXPOSE 8000

RUN mkdir -p /usr/src/app/
RUN apt-get update && apt-get install -y --no-install-recommends libmagic1 && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash web-server-user

WORKDIR /usr/src/app/

RUN mkdir backend files instance

COPY ../backend/requirements.txt backend/.
COPY ../backend/api/ backend/api
COPY ../backend/ldap-cert/ ldap-cert
COPY ../backend/startapp_server.sh startapp_server.sh

RUN python -m venv backend/venv
RUN python -m pip install -U pip
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r backend/requirements.txt

RUN chmod u+x startapp_server.sh

RUN chown -R web-server-user:web-server-user startapp_server.sh files instance

USER web-server-user

CMD sh ./startapp_server.sh