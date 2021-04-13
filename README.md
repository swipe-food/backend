# SwipeFood

## Run

1. Create a `.env` file with the following content: 

```shell
SF_ENVIRONMENT=prod
SF_API_NAME="Swipe Food API"
SF_API_HOST=localhost
SF_API_PORT=3000
SF_API_DEBUG=True
SF_API_LOG_FILE_NAME=/var/log/swipe-food/api.log
SF_API_LOG_LEVEL_CONSOLE=INFO
SF_API_LOG_LEVEL_FILE=DEBUG
SF_CRAWLER_FETCH_BATCH_SIZE=20
SF_CRAWLER_LOG_FILE_NAME=/var/log/swipe-food/crawler.log
SF_CRAWLER_LOG_LEVEL_CONSOLE=INFO
SF_CRAWLER_LOG_LEVEL_FILE=DEBUG
SF_DATABASE_DIALECT=postgresql
SF_DATABASE_DRIVER=psycopg2
SF_DATABASE_HOST=localhost
SF_DATABASE_PORT=5432
SF_DATABASE_NAME=swipe_food
SF_DATABASE_USER=sf_access_user
SF_DATABASE_PASSWORD=swipe food database password # change
SF_DATABASE_MAX_IDLE_CONNECTIONS=25
SF_DATABASE_MAX_OPEN_CONNECTIONS=25
SF_DATABASE_LOGGING_ENABLED=False
SF_DATABASE_LOGGING_LEVEL=warning
DOCKER_POSTGRES_USER=sql
DOCKER_POSTGRES_DB=sql
DOCKER_POSTGRES_PASSWORD=sql database password # change
DOCKER_PGADMIN_DEFAULT_EMAIL=admin@admin.com
DOCKER_PGADMIN_DEFAULT_PASSWORD=pgadmin password # change
```
Make sure to change the passwords.

2. Run the `api` and the `crawler` with docker-compose
```shell
docker-compose up 
```

## Domain Model

![UML Domain Model](./Assets/domain_model.png)

