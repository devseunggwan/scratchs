SELECT
    ID
    , FIRST_NAME
    , LAST_NAME
    , BIRTH_DATE
FROM
    {{ ref('customers') }}