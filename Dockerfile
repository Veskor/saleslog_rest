# python backend
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
CMD python manage.py makemigrations core_api
CMD python manage.py makemigrations accounts
CMD python manage.py makemigrations
CMD python manage.py migrate
