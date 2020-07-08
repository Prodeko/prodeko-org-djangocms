# Stage 1 - build tiedotteet frontend
FROM node:12 as tiedotteet-build
WORKDIR /app

COPY tiedotteet/frontend/package.json ./
RUN npm install

ADD tiedotteet/frontend /app
RUN npm run build:prod

# Stage 2 - main container definition
FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt requirements.txt ./
COPY requirements-dev.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements-dev.txt

RUN apt-get update && apt-get install -y postgresql-client gettext dos2unix

COPY . /code/
COPY --from=tiedotteet-build /app/public/tiedotteet /code/tiedotteet/frontend/public/tiedotteet