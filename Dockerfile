# Stage 1 - build tiedotteet frontend
FROM node:12 as tiedotteet-build
WORKDIR /app

COPY tiedotteet/frontend/package.json ./
RUN npm install

ADD tiedotteet/frontend /app
RUN npm run build:prod

# Stage 2 - main container definition
FROM python:3-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt requirements.txt ./
COPY requirements-dev.txt requirements-dev.txt ./

RUN apk add --no-cache --virtual .build-deps build-base libxslt-dev libressl-dev libffi-dev zlib-dev jpeg-dev libpng-dev musl-dev postgresql-dev && \
  apk add --no-cache libxslt postgresql-client gettext libjpeg && \
  pip install --no-cache-dir -r requirements-dev.txt && \
  apk del --purge .build-deps

COPY . /code/
COPY --from=tiedotteet-build /app/public/tiedotteet /code/tiedotteet/frontend/public/tiedotteet