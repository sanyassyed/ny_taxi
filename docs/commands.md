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
* `jupyter notebook` -> to run jupyter notebook


## SQL
SELECT COUNT(1)
FROM green_taxi_data
WHERE lpep_pickup_datetime LIKE '2019-09-18%' AND lpep_dropoff_datetime LIKE '2019-09-18%'

SELECT lpep_pickup_datetime, trip_distance
FROM green_taxi_data
ORDER BY 2 DESC
LIMIT 1

SELECT 'z.Borough', SUM(CAST('gt.total_amount' AS DOUBLE PRECISION))
FROM green_taxi_data as gt, zone as z
WHERE 'gt.PULocationID' = 'z.LocationID' AND CAST('gt.lpep_pickup_datetime' AS DATE) = '2019-09-18'
GROUP BY 1
ORDER BY 2 DESC

SELECT 'PULocationID', SUM ('total_amount'::DOUBLE PRECISION) as total
FROM green_taxi_data as gt
WHERE'gt.lpep_pickup_datetime' = '2019-09-18'
GROUP BY 1
ORDER BY 2 DESC

SELECT 'Borough', SUM(total_amount)
FROM green_taxi_data, zone
WHERE lpep_pickup_datetime LIKE '2019-09-18%' AND 'PULocationID' = 'LocationID'
GROUP BY 'Borough'
ORDER BY 2 DESC