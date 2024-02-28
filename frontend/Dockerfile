FROM node:18.16.1

EXPOSE 3000

RUN useradd -ms /bin/bash web-client-user

RUN mkdir -p /usr/src/app/frontend/
WORKDIR /usr/src/app/frontend/

COPY ../frontend .

RUN chown -R web-client-user:web-client-user /usr/src/app/frontend

USER web-client-user

RUN npm install
RUN npm run build-prod

CMD npm run local-deploy