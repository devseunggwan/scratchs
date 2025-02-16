from airflowm.decorators import dag, task
from datetime import datetime


@dag(
    dag_id="etl-pipeline",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
)
def etl_pipeline():
    @task
    def extract():
        data = {"orders": [100, 200, 300]}
        print("Data Extracted")

        return data

    @task
    def transform(data: dict):
        data = {"total_orders": sum(data["orders"])}
        print("Data Transformed")

        return data

    @task
    def load(data: dict):
        print(f"Data Loaded: {data}")

    __data = extract()
    __data = transform(__data)
    load(__data)


etl_dag = etl_pipeline()
