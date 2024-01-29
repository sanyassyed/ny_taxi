# Homework Solutions and working
## WEEK 1 Docker & Terraform
### SQL Statements

* Q3: How many taxi trips were totally made on September 18th 2019?
    ```sql
    SELECT 
        COUNT(1)
    FROM 
        green_taxi_data
    WHERE 
        lpep_pickup_datetime LIKE '2019-09-18%' AND 
        lpep_dropoff_datetime LIKE '2019-09-18%'
    ```

* Q4: Which was the pick up day with the largest trip distance Use the pick up time for your calculations.
    ```sql
    SELECT 
        lpep_pickup_datetime, trip_distance
    FROM 
        green_taxi_data
    ORDER BY 2 DESC
    LIMIT 1
    ```
* Q5: Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
    ```sql
    SELECT 
        "Borough", 
        SUM("total_amount") as total
    FROM 
        green_taxi_data, zone
    WHERE 
        "lpep_pickup_datetime" LIKE '2019-09-18%' AND 
        "PULocationID" = "LocationID" AND 
        "Borough" NOT LIKE 'Unknown' 
    GROUP BY 1
    HAVING 
        SUM("total_amount") > 50000
    ORDER BY 2 DESC
    ```

* Q6: For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip? We want the name of the zone, not the id.
    ```sql
    --Option 1
    SELECT 
        z2."Zone" as DropOffBorough, 
        MAX("tip_amount")
    FROM 
        green_taxi_data, zone z1, zone z2
    WHERE 
        "PULocationID" = z1."LocationID" AND 
        "DOLocationID" = z2."LocationID" AND
        z1."Zone" LIKE 'Astoria'
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 5

    --Option 2
    SELECT 
        z2."Zone" as dropOffBorough, 
        "tip_amount"
    FROM 
        green_taxi_data, zone z1, zone z2
    WHERE 
        "PULocationID" = z1."LocationID" AND 
        "DOLocationID" = z2."LocationID" AND
        z1."Zone" LIKE 'Astoria'
    ORDER BY 2 DESC
    LIMIT 5
    ```





