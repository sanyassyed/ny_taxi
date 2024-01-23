# Commands used in this project

## Docker
### 1.2.2
* for Postgres via cli
docker run -it \
    -e POSTGRES_USER="codespace" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/db_data:/var/lib/postgresql/data \
    -p 5432:5432 \
postgres:13

* enter the db
`pgcli -h localhost -p 5432 -u codespace -d ny_taxi`

## Linux
* `ls -lah` -> to check the permissions for the folders
* `sudo chown codespace:codespace db_data` -> to change the owner of the folder db_data