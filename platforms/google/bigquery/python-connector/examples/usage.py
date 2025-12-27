"""BigQuery Connector 사용 예시."""

from dotenv import load_dotenv

load_dotenv()

from connector import AuthMethod, BigQueryConfig, BigQueryConnector


def example_basic_usage():
    """기본 사용법."""
    config = BigQueryConfig(
        project_id="my-gcp-project",
        auth_method=AuthMethod.ADC,
        location="asia-northeast3",
    )

    connector = BigQueryConnector(config)

    # 기본 쿼리 실행
    rows = connector.execute("SELECT 1 as num, 'hello' as msg")
    print("Raw results:", rows)

    # Pandas DataFrame
    df = connector.to_pandas(
        "SELECT * FROM `bigquery-public-data.samples.shakespeare` LIMIT 10"
    )
    print("\nPandas DataFrame:")
    print(df)

    connector.close()


def example_from_env():
    """환경변수에서 설정 로드."""
    with BigQueryConnector.from_env() as connector:
        df = connector.to_pandas(
            "SELECT word, word_count FROM `bigquery-public-data.samples.shakespeare` "
            "ORDER BY word_count DESC LIMIT 10"
        )
        print(df)


def example_with_polars():
    """Polars DataFrame 사용."""
    with BigQueryConnector.from_env() as connector:
        df_polars = connector.to_polars(
            "SELECT * FROM `bigquery-public-data.samples.shakespeare` LIMIT 100"
        )
        print(type(df_polars))
        print(df_polars)


def example_parameterized_query():
    """파라미터 쿼리."""
    with BigQueryConnector.from_env() as connector:
        df = connector.to_pandas(
            """
            SELECT word, word_count
            FROM `bigquery-public-data.samples.shakespeare`
            WHERE corpus = @corpus_name
            LIMIT 10
            """,
            params={"corpus_name": "hamlet"},
        )
        print(df)


def example_dry_run():
    """쿼리 검증 및 비용 추정."""
    with BigQueryConnector.from_env() as connector:
        result = connector.dry_run(
            "SELECT * FROM `bigquery-public-data.samples.shakespeare`"
        )
        print("Dry run result:")
        print(f"  Valid: {result['valid']}")
        if result["valid"]:
            print(f"  Bytes to process: {result['bytes_processed_human']}")
            print(f"  Estimated cost: ${result['estimated_cost_usd']}")


def example_schema_and_metadata():
    """스키마 및 메타데이터 조회."""
    with BigQueryConnector.from_env() as connector:
        # 데이터셋 목록
        datasets = connector.list_datasets()
        print("Datasets:", datasets[:5] if len(datasets) > 5 else datasets)

        # 테이블 스키마 (public dataset)
        schema = connector.get_schema("bigquery-public-data.samples.shakespeare")
        print("\nSchema:")
        for field in schema:
            print(f"  {field.name}: {field.field_type}")


def example_large_data_with_iterator():
    """대용량 데이터 처리 (Iterator)."""
    with BigQueryConnector.from_env() as connector:
        count = 0
        for row in connector.execute_iter(
            "SELECT * FROM `bigquery-public-data.samples.shakespeare` LIMIT 10000",
            page_size=1000,
        ):
            count += 1
            if count <= 3:
                print(row)
        print(f"Total rows: {count}")


def example_service_account():
    """서비스 계정 인증."""
    config = BigQueryConfig(
        project_id="my-gcp-project",
        auth_method=AuthMethod.SERVICE_ACCOUNT,
        credentials_path="./credentials/service-account.json",
    )

    with BigQueryConnector(config) as connector:
        df = connector.to_pandas("SELECT 1")
        print(df)


if __name__ == "__main__":
    print("=== Basic Usage (from env) ===")
    example_from_env()

    print("\n=== Dry Run ===")
    example_dry_run()

    print("\n=== Schema ===")
    example_schema_and_metadata()
