FROM python:3.6.7

RUN apt-get -q update && apt-get install -y -q \
  sqlite3 --no-install-recommends \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG C.UTF-8

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install --no-cache-dir -r saleslog_rest/requirements.txt

CMD gunicorn -b :8000 saleslog_rest.wsgi
