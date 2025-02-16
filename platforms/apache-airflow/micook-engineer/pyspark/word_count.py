import os
from pyspark.sql import SparkSession

def word_count(input_path: str, output_path: str):
    spark = SparkSession.builder.appName("WordCount") \
            .config("fs.s3a.access.key", "ROOTNAME") \
            .config("fs.s3a.secret.key", "CHANGEME123") \
            .config("fs.s3a.endpoint", "http://minio:9000") \
            .config("fs.s3a.connection.ssl.enabled", "false") \
            .config("fs.s3a.path.style.access", "true") \
            .config("fs.s3a.attempts.maximum", "1") \
            .config("fs.s3a.connection.establish.timeout", "5000") \
            .config("fs.s3a.connection.timeout", "10000") \
        .getOrCreate()
    text_file = spark.read.text(f"{input_path}")
    # How it works
    # -> "Lorem ipsum dolor sit amet sit ..."
    # -> ('Lorem', 1), ('ipsum', 1), ('dolor', 1), ('sit', 1), ('amet', 1), ('sit', 1)
    # -> ('Lorem', 1), ('ipsum', 1), ('dolor', 1), ('sit', (1 + 1)), ('amet', 1)
    # -> ('Lorem', 1), ('ipsum', 1), ('dolor', 1), ('sit', 2), ('amet', 1)
    counts = (
        text_file.rdd.flatMap(lambda line: line[0].split())
        .map(lambda word: (word, 1))
        .reduceByKey(lambda a, b: a + b)
    )
    counts.toDF(["word", "count"]).write.csv(f"{output_path}", header=True)
    spark.stop()

if __name__ == "__main__":
    import sys
    word_count(sys.argv[1], sys.argv[2])

# # SparkSubmit Command
# spark-submit \
# --master spark://spark:7077 \
# --deploy-mode client \
# --name WordCountApp \
# --executor-memory 1G \
# --total-executor-cores 2 \
# --packages org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
# /opt/bitnami/spark/work/pyspark/word_count.py \
# s3a://word-count/input.txt \
# s3a://word-count/output
