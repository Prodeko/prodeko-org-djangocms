# Stage 1 - build tiedotteet frontend
FROM node:12 as tiedotteet-build
WORKDIR /app

COPY tiedotteet/frontend/package.json tiedotteet/frontend/package-lock.json ./
RUN npm ci

ADD tiedotteet/frontend /app
RUN npm run build:prod

# Stage 2 - main container definition
FROM python:3.10.0b3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements*.txt /app/
RUN pip install --no-cache-dir -r requirements-dev.txt

RUN apt-get update && apt-get install -y postgresql-client gettext dos2unix \
  && rm -rf /var/lib/apt/lists/*

COPY . /app/
COPY --from=tiedotteet-build /app/public/tiedotteet /app/tiedotteet/frontend/public/tiedotteet