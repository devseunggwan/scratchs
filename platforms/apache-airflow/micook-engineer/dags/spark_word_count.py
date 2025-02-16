from datetime import datetime

from airflow.decorators import dag
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.slakck.notifications.slack_notifier import SlackNotifier


default_args = {
    "owner": "devseunggwan",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "retries": 1,
}

dag_args = {
    "default_args": default_args,
    "description": "DAG to run Spark Word Count job using Taskflow API and SparkSubmitOperator",
    "schedule_interval": None,
    "catchup": False,
    "on_success_callback": SlackNotifier(
        slack_conn_id="slack_default",
        text="Spark DAG has successed",
        channel="#general",
    ),
    "on_failure_callback": SlackNotifier(
        slack_conn_id="slack_default", text="Spark DAG has failed", channel="#general"
    ),
}


@dag(*dag_args)
def spark_word_count_taskflow():
    check_minio_file = S3KeySensor(
        task_id="check_minio_file",
        bucket_name="word-count",
        bucket_key="input.txt",
        aws_conn_id="minio_default",
    )

    spark_task = SparkSubmitOperator(
        task_id="spark_submit_task",
        name="WorkCountApp",
        executor_memory="1G",
        total_executor_cores=2,
        application="/opt/bitnami/spark/work/pyspark/word_count.py",
        conn_id="spark_default",
        application_args=["s3a://word-count/input.txt", "s3a://word-count/output"],
        packages="org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262",
    )

    check_minio_file >> spark_task


spark_word_count_dag = spark_word_count_taskflow()
