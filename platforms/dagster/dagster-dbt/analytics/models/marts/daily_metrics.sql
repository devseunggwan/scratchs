{{
    config(
        materialized='incremental',
        unique_key='date_of_business'
    )
}}

with 
    trips as (
        SELECT
            *
        FROM
            {{ ref('stg_trips') }}
    ),
    daily_summary as (
        SELECT
            date_trunc('day', pickup_datetime) as date_of_business,
            count(*) as trip_count,
            sum(duration) as total_duration,
            sum(duration) / count(*) as average_duration,
            sum(total_amount) as total_amount,
            sum(total_amount) / count(*) as average_amount,
            sum(case when duration > 30 then 1 else 0) / count(*) as pct_over_30_min
        FROM
            trips
        GROUP BY
            all
    )
SELECT
    *
FROM
    daily_summary
{% if is_incremental() %}
    WHERE date_of_business between {{ var('min_date') }} and {{ var('max_date') }}
{% endif %}