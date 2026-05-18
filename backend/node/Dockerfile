# Dockerfile for Node.js API Gateway
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

ENV NODE_ENV=production
EXPOSE 4000
ENV NODE_PORT=4000

CMD ["npm", "run", "start"]
