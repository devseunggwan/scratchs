import os

import duckdb
import requests
from dagster import asset
from dagster._utils.backoff import backoff

from . import constants


@asset
def taxi_trips_file() -> None:
    """The raw parquet files for the taxi trips dataset. Sourced from the NYC Open Data portal."""
    month_to_fetch = "2023-03"

    __url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet"
    __resp = requests.get(__url.format(month_to_fetch=month_to_fetch))

    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), "wb") as output_file:
        output_file.write(__resp.content)


@asset
def texi_zone_file() -> None:
    """The raw CSV file for the taxi zones dataset. Sourced from the NYC Open Data portal."""

    __url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
    __resp = requests.get(__url)

    with open(constants.TAXI_ZONES_FILE_PATH, "wb") as output_file:
        output_file.write(__resp.content)


@asset(deps=["taxi_trips_file"])
def texi_trips() -> None:
    __query = """
        create or replace table trips as (
            SELECT
                VendorID as vendor_id,
                PULocationID as pickup_zone_id,
                DOLocationID as dropoff_zone_id,
                RatecodeID as rate_code_id,
                payment_type as payment_type,
                tpep_dropoff_datetime as dropoff_datetime,
                tpep_pickup_datetime as pickup_datetime,
                trip_distance as trip_distance,
                passenger_count as passenger_count,
                total_amount as total_amount
            FROM
                'data/raw/taxi_trips_2023-03.parquet'
        );
    """

    __conn = backoff(
        fn=duckdb.connect,
        retry_on=(RuntimeError, duckdb.IOException),
        kwargs={"database": os.getenv("DUCKDB_DATABASE")},
        max_retries=10,
    )
    __conn.execute(__query)


@asset(deps=["texi_zone_file"])
def texi_zones() -> None:
    __query = f"""
        create or replace table zones as (
            SELECT
                LocationID as zone_id,
                Zone as zone,
                Borough as borough,
                service_zone
            FROM
                '{constants.TAXI_ZONES_FILE_PATH}'
        );
    """

    __conn = backoff(
        fn=duckdb.connect,
        retry_on=(RuntimeError, duckdb.IOException),
        kwargs={"database": os.getenv("DUCKDB_DATABASE")},
        max_retries=10,
    )
    __conn.execute(__query)
