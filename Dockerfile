# Stage 1 - build tiedotteet frontend
FROM node:10 as tiedotteet-build
WORKDIR /app
COPY tiedotteet/frontend/package.json ./
RUN npm install
ADD tiedotteet/frontend /app
RUN npm run build:dev

# Stage 2 - main container definition
FROM python:3

ENV PYTHONUNBUFFERED 1

# Install Python and Package Libraries
RUN apt-get update && \
    apt-get install -y mysql-client gettext

RUN apt-get update && apt-get install -y dos2unix

WORKDIR /code

COPY requirements.txt requirements.txt ./
RUN pip install -r requirements.txt

COPY . /code/
COPY --from=tiedotteet-build /app/public/tiedotteet /code/tiedotteet/frontend/public/tiedotteet
COPY docker-entrypoint.sh /usr/local/bin/
RUN dos2unix /usr/local/bin/docker-entrypoint.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]