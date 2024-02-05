FROM python:3.9.1

RUN apt-get install wget
RUN pip install pyarrow pandas sqlalchemy psycopg2

WORKDIR /app
RUN mkdir data
COPY pipeline.py pipeline.py

ENTRYPOINT ["python", "pipeline.py"]

# docker-conatiner for postgres
# docker run -it \
#     -e POSTGRES_USER="codespace" \
#     -e POSTGRES_PASSWORD="root" \
#     -e POSTGRES_DB="ny_taxi" \
#     -v $(pwd)/db_data:/var/lib/postgresql/data \
#     -p 5432:5432 \
#     --network=pg-network \
#     --name=pg-database \
# postgres:13

# docker container for the ETL pipeline
# docker build -t taxi_ingest:v001 .
# docker run -it \
#     --network=pg-network \
# taxi_ingest:v001 \
#     --user=codespace \
#     --password=root \
#     --host=pg-database \
#     --port=5432 \
#     --db=ny_taxi \
#     --taxi_color=yellow \
#     --year=2021 \
#     --month=9

