FROM node:18.16.1

EXPOSE 3000

RUN mkdir -p /usr/src/app/frontend/
WORKDIR /usr/src/app/frontend/

COPY ../frontend .

RUN npm install
RUN npm run build-prod

CMD npm run local-deploy