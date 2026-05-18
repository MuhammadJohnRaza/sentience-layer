# Dockerfile for Next.js Web Frontend
FROM node:18-alpine AS base

# Install dependencies only when needed
WORKDIR /app
COPY package*.json ./
RUN npm install --frozen-lockfile

# Rebuild the source code only when needed
COPY . .
RUN npm run build

# Production image, copy all the files and run next
ENV NODE_ENV=production
EXPOSE 3000
ENV PORT=3000

CMD ["npm", "run", "start"]
