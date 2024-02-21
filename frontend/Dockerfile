FROM node:18.16.1

EXPOSE 3000

RUN mkdir -p /usr/src/app/frontend/
WORKDIR /usr/src/app/frontend/

COPY ../frontend/src src
COPY ../frontend/.browserslistrc .browserslistrc
COPY ../frontend/global.d.ts global.d.ts
COPY ../frontend/package.json package.json
COPY ../frontend/tsconfig.json tsconfig.json
COPY ../frontend/webpack.config.js webpack.config.js

RUN npm install
RUN npm run build-prod

CMD npm run local-deploy