import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dagster import AssetExecutionContext, asset
from dagster_duckdb import DuckDBResource

from ..partitions import weekly_partition
from . import constants


@asset(deps=["taxi_trips", "taxi_zones"])
def manhattan_stats(database: DuckDBResource) -> None:
    __query = """
        select
            zones.zone,
            zones.borough,
            zones.geometry,
            count(1) as num_trips,
        from trips
        left join zones on trips.pickup_zone_id = zones.zone_id
        where borough = 'Manhattan' and geometry is not null
        group by zone, borough, geometry
    
    """
    with database.connection() as __conn:
        trips_by_zone = __conn.execute(__query).fetch_df()

    trips_by_zone["geometry"] = gpd.GeoSeries.from_wkt(trips_by_zone["geometry"])
    trips_by_zone = gpd.GeoDataFrame(trips_by_zone)

    with open(constants.MANHATTAN_STATS_FILE_PATH, "w") as output_files:
        output_files.write(trips_by_zone.to_json())


@asset(deps=["manhattan_stats"])
def manhattan_map() -> None:
    trips_by_zone = gpd.read_file(constants.MANHATTAN_STATS_FILE_PATH)

    fig = px.choropleth_mapbox(
        trips_by_zone,
        geojson=trips_by_zone.geometry.__geo_interface__,
        locations=trips_by_zone.index,
        color="num_trips",
        color_continuous_scale="Plasma",
        mapbox_style="carto-position",
        center={"lat": 40.768, "lon": -73.985},
        zoom=11,
        opacity=0.7,
        labels={"num_trips": "Number of Trips"},
    )

    pio.write_image(fig, constants.MANHATTAN_MAP_FILE_PATH)


@asset(deps=["taxi_trips"], partitions_def=weekly_partition)
def trips_by_week(context: AssetExecutionContext, database: DuckDBResource) -> None:
    period_to_fetch = context.partition_key

    query = f"""
        SELECT vendor_id,
               total_amount,
               trip_distance,
               passenger_count
          FROM trips
         WHERE 1=1
           AND pickup_datetime >= '{period_to_fetch}'
           AND pickup_datetime <  '{period_to_fetch}'::date + INTERVAL '1 week'
    ;
    """

    with database.get_connection() as __conn:
        date_for_week = __conn.execute(query).fetch_df()

    aggregate = (
        date_for_week.agg(
            {"vendor_id": "count", "total_amount": "sum", "trip_distance": "sum", "passenger_count": "sum"}
        )
        .rename({"vendor_id": "num_trips"})
        .to_frame()
        .T
    )

    aggregate["period"] = period_to_fetch
    aggregate["num_trips"] = aggregate["num_trips"].astype(int)
    aggregate["passenger_count"] = aggregate["passenger_count"].astype(int)
    aggregate["total_amount"] = aggregate["total_amount"].round(2).astype(float)
    aggregate["trip_distance"] = aggregate["trip_distance"].round(2).astype(float)
    aggregate = aggregate[["period", "num_trips", "total_amount", "trip_distance", "passenger_count"]]

    try:
        existing = pd.read_csv(constants.TRIPS_BY_WEEK_FILE_PATH)
        existing = existing[existing["period"] != period_to_fetch]
        existing = pd.concat([existing, aggregate]).sort_values(by="period")
        existing.to_csv(constants.TRIPS_BY_WEEK_FILE_PATH, index=False)
    except FileNotFoundError:
        aggregate.to_csv(constants.TRIPS_BY_WEEK_FILE_PATH, index=False)
