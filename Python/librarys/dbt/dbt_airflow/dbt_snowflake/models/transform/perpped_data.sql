SELECT
    A.ID
    , FIRST_NAME
    , LAST_NAME
    , BIRTH_DATE
    , BOOKING_REFERENCE
    , HOTEL
    , BOOKING_DATE
    , COST
FROM
    {{ ref('customer') }} A
JOIN
    {{ ref('combined_bookings') }} B
    ON A.ID = B.ID