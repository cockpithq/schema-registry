# Schema Registry

## Deployment
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/cockpithq/schema-registry/tree/heroku-deploy-button)

After successfully deployed – create superuser:
```shell
heroku run python manage.py createsuperuser
```

For usage – check swagger page:
https://YOURAPP.herokuapp.com/docs/api/v1/swagger-ui/

## Development

### Linting
```shell
docker compose run --rm web flake8
```
### Run mypy
```shell
docker compose run --rm web mypy schema_registry
```
### Run unit tests
```shell
docker compose run --rm web pytest
```
### Run a Django development web server
```shell
docker compose up web
```
