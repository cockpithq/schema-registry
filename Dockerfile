FROM python:3.10 as base
ENV SRC_PROJECT_PATH /src
RUN mkdir -p $SRC_PROJECT_PATH
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system
WORKDIR $SRC_PROJECT_PATH

FROM base as dev
RUN pipenv install --deploy --system --dev
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base as prod
RUN pip install gunicorn
COPY ./src $SRC_PROJECT_PATH/
CMD ["gunicorn", "schema_registry.wsgi", "--bind", "0.0.0.0:80"]