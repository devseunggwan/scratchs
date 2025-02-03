import base64

import plotly.express as px
import plotly.io as pio
from dagster import Config, MaterializeResult, MetadataValue, asset
from dagster_duckdb import DuckDBResource

from . import constants


class AdhocRequestConfig(Config):
    filename: str
    borough: str
    start_date: str
    end_date: str


@asset(deps=["taxi_zones", "taxi_trips"])
def adhoc_request(config: AdhocRequestConfig, database: DuckDBResource) -> None:
    __file_path = constants.REQUEST_DESTINATION_TEMPLATE_FILE_PATH.format(config.filename.split(".")[0])
    __query = f"""
        SELECT DATE_PART('hour', pickup_datetime) as hour_of_day,
               DATE_PART('dayofweek', pickup_datetime) as day_of_week_num,
               CASE DATE_PART('dayofweek', pickup_datetime)
                   WHEN 0 THEN 'Sunday'
                   WHEN 1 THEN 'Monday'
                   WHEN 2 THEN 'Tuesday'
                   WHEN 3 THEN 'Wednesday'
                   WHEN 4 THEN 'Thursday'
                   WHEN 5 THEN 'Friday'
                   WHEN 6 THEN 'Saturday
               END AS day_of_week,
               COUNT(*) AS num_trips
          FROM trips
          LEFT
          JOIN zones
            ON trips.pickup_zone_id = zones.zone_id
         WHERE 1=1
           AND pickup_datetime >= '{config.start_date}'
           AND pickup_datetime <  '{config.end_date}'
           AND pickup_zone_id  in (
               SELECT zone_id
                 FROM zones
                WHERE borough = '{config.borough}'
               )
         GROUP
            BY 1, 2
         ORDER
            BY 1, 2
    ;
    """

    with database.get_connection() as __conn:
        results = __conn.execute(__query).fetch_df()

    fig = px.bar(
        results,
        x="hour_of_day",
        y="num_trips",
        color="day_of_week",
        barmode="stack",
        title=f"Number of trips by hour of day in {config.borough}, from {config.start_date} to {config.end_date}",
        labels={"hour_of_day": "Hour of Day", "day_of_week": "Day of Week", "num_trips": "Number of Trips"},
    )

    pio.write_image(fig, __file_path)

    with open(__file_path, "rb") as file:
        image_data = file.read()

    base64_data = base64.b64encode(image_data).decode("utf-8")
    md_content = f"![Image](data:image/jpeg;base64, {base64_data})"

    return MaterializeResult(metadata={"preview": MetadataValue.md(md_content)})
