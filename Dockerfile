FROM python:3.10 as base
RUN pip install pipenv==2021.11.23
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system
ENV SRC_PROJECT_PATH /app
RUN mkdir -p $SRC_PROJECT_PATH
WORKDIR $SRC_PROJECT_PATH

FROM base as dev
RUN pipenv install --deploy --system --dev
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base as prod
RUN pip install gunicorn==20.1.0
COPY ./schema_registry $SRC_PROJECT_PATH/schema_registry
COPY ./manage.py $SRC_PROJECT_PATH
CMD ["gunicorn", "schema_registry.wsgi", "--bind", "0.0.0.0:80"]

FROM base as heroku
RUN pip install gunicorn==20.1.0 whitenoise==6.2.0
COPY ./schema_registry $SRC_PROJECT_PATH/schema_registry
COPY ./manage.py $SRC_PROJECT_PATH
COPY heroku-release.sh ./
CMD gunicorn schema_registry.wsgi:application --bind 0.0.0.0:$PORT
