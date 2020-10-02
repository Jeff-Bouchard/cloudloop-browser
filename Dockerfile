FROM node:13.12.0-alpine

# WORKDIR /app

ENV PATH /node_modules/.bin:$PATH

COPY package.json ./
COPY yarn.lock ./
RUN yarn install
RUN yarn add react-scripts@3.4.1 -g

COPY . ./

CMD ["npm", "start"]
