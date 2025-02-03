import pandas as pd
import requests
from dagster import AssetExecutionContext, MaterializeResult, MetadataValue, asset
from dagster_duckdb import DuckDBResource

from ..partitions import monthly_partition
from . import constants


@asset(partitions_def=monthly_partition, group_name="raw_files")
def taxi_trips_file(context: AssetExecutionContext) -> MaterializeResult:
    """The raw parquet files for the taxi trips dataset. Sourced from the NYC Open Data portal."""

    partition_date_str = context.partition_key
    # month_to_fetch = "2023-03"
    month_to_fetch = partition_date_str[:-3]

    __url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet"
    __resp = requests.get(__url.format(month_to_fetch=month_to_fetch))

    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), "wb") as output_file:
        output_file.write(__resp.content)

    num_rows = len(pd.read_parquet(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch)))

    return MaterializeResult(metadata={"Number of records": MetadataValue.int(num_rows)})


@asset(
    description="The raw CSV file for the taxi zones dataset. Sourced from the NYC Open Data portal.",
    group_name="raw_files",
)
def taxi_zone_file() -> MaterializeResult:
    __url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
    __resp = requests.get(__url)

    with open(constants.TAXI_ZONES_FILE_PATH, "wb") as output_file:
        output_file.write(__resp.content)

    num_rows = len(pd.read_parquet(constants.TAXI_ZONES_FILE_PATH))

    return MaterializeResult(metadata={"Number of records": MetadataValue.int(num_rows)})


@asset(deps=["taxi_trips_file"], partitions_def=monthly_partition, group_name="ingested")
def taxi_trips(context: AssetExecutionContext, database: DuckDBResource) -> None:
    partition_date_str = context.partition_key
    month_to_fetch = partition_date_str[:-3]

    __query = f"""
        CREATE TABLE IF NOT EXISTS trips (
            vendor_id integer,
            pickup_zone_id integer,
            dropoff_zone_id integer,
            rate_code_id double,
            payment_type integer,
            dropoff_datetime timestamp,
            pickup_datetime timestamp,
            trip_distance double,
            passenger_count double,
            total_amount double,
            partition_date varchar
        );
        
        DELETE
          FROM trips
         WHERE partition_date = '{month_to_fetch}'
        ;
        
        INSERT
          INTO trips
        SELECT VendorID,
               PULocationID,
               DOLocationID,
               RatecodeID,
               payment_type,
               tpep_dropoff_datetime,
               tpep_pickup_datetime,
               trip_distance,
               passenger_count,
               total_amount,
               '{month_to_fetch}' as partition_date
          FROM '{constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch)}'
        ;
    """

    with database.get_connection() as __conn:
        __conn.execute(__query)


@asset(deps=["taxi_zone_file"], group_name="ingested")
def taxi_zones(database: DuckDBResource) -> None:
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

    with database.get_connection() as __conn:
        __conn.execute(__query)
