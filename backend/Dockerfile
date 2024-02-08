FROM python:3.8

ENV PYDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

RUN mkdir backend

COPY requirements.txt backend/.
COPY .env backend/.
COPY api/ backend/api
COPY startapp.sh startapp.sh

RUN python -m venv backend/venv
RUN python -m pip install -r backend/requirements.txt

RUN chmod u+x startapp.sh

CMD ["sh", "./startapp.sh"]