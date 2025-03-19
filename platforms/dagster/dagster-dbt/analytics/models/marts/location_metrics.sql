with
    trips as (
        SELECT
            *
        FROM
            {{ ref('stg_trips') }}
    ),
    zones as (
        SELECT
            *
        FROM
            {{ ref('stg_zones') }}
    ),
    trips_by_zone as (
        SELECT
            pick~up_zones.zone_name as zone,
            dropoff_zones.borough as destination_borough,
            pickup_zones.is_airport as from_airport,
            count(*) as trips,
            sum(trips.trip_distance) as total_distance,
            sum(trips.duration) as total_duration,
            sum(trips.total_amount) as fare,
            sum(case when duration > 30 then 1 else 0 end) as trips_over_30_min
        FROM
            trips
        LEFT JOIN zones as pickup_zones on trip.pickup_zone_id = pickup_zone.zone_id
        LEFT JOIN zones as dropoff_zones on trip.dropoff_zone_id = dropoff_zones.zone_id
        GROUP BY
            all
    )
SELECT
    *
FROM
    trips_by_zone
;