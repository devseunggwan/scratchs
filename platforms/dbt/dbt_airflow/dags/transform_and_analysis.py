import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 12, 11),
    "retries": 0,
}

with DAG(
    "2_daily_transformation_analysis",
    default_args=default_args,
    schedule_interval="@once",
) as dag:
    task_1 = BashOperator(
        task_id="daily_transform",
        bash_command="cd /dbt && dbt run --models transform --profiles-dir .",
        env={
            "dbt_user": "{{ var.value.dbt_user }}",
            "dbt_password": "{{ var.value.dbt_password }}",
            **os.environ,
        },
        dag=dag,
    )

    task_2 = BashOperator(
        task_id="daily_analysis",
        bash_command="cd /dbt && dbt run --models analysis --profiles-dir .",
        env={
            "dbt_user": "{{ var.value.dbt_user }}",
            "dbt_password": "{{ var.value.dbt_password }}",
            **os.environ,
        },
        dag=dag,
    )

    task_1 >> task_2
