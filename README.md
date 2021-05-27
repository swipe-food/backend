# SwipeFood

[![Swipe Food Backend Test](https://github.com/swipe-food/backend/actions/workflows/test_ci_pipeline.yml/badge.svg)](https://github.com/swipe-food/backend/actions/workflows/test_ci_pipeline.yml)
[![Swipe Food Docker Image CI](https://github.com/swipe-food/backend/actions/workflows/docker_build_and_deploy.yml/badge.svg)](https://github.com/swipe-food/backend/actions/workflows/docker_build_and_deploy.yml)
[![codecov](https://codecov.io/gh/swipe-food/backend/branch/main/graph/badge.svg?token=R7OUWH58L2)](https://codecov.io/gh/swipe-food/backend)

## Run

### Local

1. Run the Postgres (optional with pgAdmin)
```shell
docker-compose up postgres pgadmin
```

2. Create a `local.env` file with all necessary environmental variables. Have a look at the `example.local.env` file.

3. Run the API and/or the Crawler
```shell
python3 -m main.api
python3 -m main.crawler
```

### Docker Compose

1. Create a `dkc.env` file with all necessary environmental variables. Have a look at the `example.dkc.env` file. The only difference to the previous `example.local.env` file is that the host of the Postgres database is the `postgres` container itself.


2. Run the complete application (API, Crawler, Postgres DB, pgAdmin) 
```shell
docker-compose --env-file=dkc.env up 
```

## Domain Model

![UML Domain Model](./Assets/domain_model.png)

## Development

For dependency management pip is used in combination with [pip-tools](https://github.com/jazzband/pip-tools).

Install:
```shell
python3 -m pip install pip-tools
```

Add new dependencies to the ``requirements.in`` file and keep the `requirements.txt` file update with the `pip-compile` command. Sync your installed dependencies with the `pip-sync` command.

## Postman Collection

The `Swipe Food API.postman_collection.json` file in the Assets directory is a Postman Collection for the API. The Requests of the Collection heavily use Collection Variables (Swipe Food API -> Edit -> Variables). These variables are mostly set by the responses of "get all" Requests (See the Tests Tab of the Request). Below is a list of all Collection Variables and the associated API Request where they are set:

|  Collection Variable | API-Request where this Variable is set |
|---|---|
| VENDOR_ID  | Vendor / get all vendors |
| VENDOR_NAME  | Vendor / get all vendors |
| CATEGORY_ID  | Category / get all categories |
| CATEGORY_NAME  | Category / get all categories |
| MATCH_ID  | User / get matches for user  |
| USER_ID  | User / get all users |
| USER_EMAIL  | User / get all users |
| RECIPE_ID  | Category / get recipes for category |
| RECIPE_NAME  | Category / get recipes for category |
| CURRENT_TIMESTAMP  | User / post user (Pre-Request Script)  |
| LANGUAGE_ID  | Languages / get all languages |
| CATEGORY_LIKE_ID  | User / get liked categories for user |
