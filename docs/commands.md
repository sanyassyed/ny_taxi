# Commands used in this project

## Docker
### 1.2.2

docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/db_database:/var/lib/postgresql/data \
    -p 5432:5432
postgres:13