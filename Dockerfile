FROM python:3

ENV PYTHONUNBUFFERED 1

# Install Python and Package Libraries
RUN apt-get update && \
      apt-get install -y mysql-client

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /code/

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]