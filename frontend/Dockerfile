FROM node:lts-alpine3.20

WORKDIR /app

COPY frontend/package*.json ./

RUN npm install && npm install --only=dev

COPY frontend/ ./

#RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "dev"]
