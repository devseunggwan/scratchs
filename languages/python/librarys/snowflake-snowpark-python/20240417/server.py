import os

from fastapi import FastAPI
from dotenv import load_dotenv
from snowflake.snowpark import Session
from datetime import datetime

load_dotenv()

# Snowflake 연결 설정
connection_parameters = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),  # optional
    "warehouse": os.getenv("SNOWFLAKE_WH"),  # optional
    "database": os.getenv("SNOWFLAKE_DATABASE"),  # optional
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),  # optional
}
new_session = Session.builder.configs(connection_parameters).create()
# Snowflake에 연결

app = FastAPI()

QUERY = """
"""


@app.get("/test")
async def sample(from_currency, to_currency):
    __from = (
        new_session.sql(
            QUERY, params=["USD" if from_currency == "KRW" else from_currency]
        )
        .to_pandas()
        .to_dict(orient="records")[0]
    )
    __to = (
        new_session.sql(QUERY, params=["USD" if to_currency == "KRW" else to_currency])
        .to_pandas()
        .to_dict(orient="records")[0]
    )

    __from_price = (
        __from["USD_PRICE"] / __from["KRW_PRICE"]
        if from_currency == "KRW"
        else __from["USD_PRICE"]
    )
    __to_price = (
        __to["USD_PRICE"] / __to["KRW_PRICE"]
        if to_currency == "KRW"
        else __to["USD_PRICE"]
    )
    __to_price = float(__from_price / __to_price)

    # DataFrame을 딕셔너리로 변환
    date, time = datetime.now().strftime("%Y%m%d %H%M%S").split(" ")

    data = {
        "date": date,
        "time": time,
        "fromCurrency": from_currency,
        "fromPrice": 1,
        "toCurrency": to_currency,
        "toPrice": __to_price,
    }

    return data
