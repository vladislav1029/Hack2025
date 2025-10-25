FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5184
ENV NUXT_PORT=$PORT
ENV PROXY_LOGIN=$PROXY_LOGIN
CMD ["npm", "start"]
