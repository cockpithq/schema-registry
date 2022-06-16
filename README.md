# Schema Registry
![Test](https://github.com/cockpithq/schema-registry/actions/workflows/test.yml/badge.svg)

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
