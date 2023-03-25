FROM node:16.15
WORKDIR /app
COPY /traffic_count/package.json .
COPY /traffic_count/package-lock.json .
RUN npm install
COPY /traffic_count .
EXPOSE 3000