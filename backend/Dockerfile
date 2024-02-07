FROM python:3.8

ENV PYDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

EXPOSE 8081

COPY venv/ venv
COPY api/ api

#RUN #source venv/bin/activate
#CMD ["ls", "/usr/src/app/venv/bin/", "-al"]
#CMD ["/usr/src/app/venv/bin/gunicorn", "--workers", "6", "--bind", "0.0.0.0:8081", "api.app"]
CMD /usr/src/app/venv/bin/gunicorn --workers 6 --bind 0.0.0.0:8081 api.app