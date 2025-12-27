"""BigQuery Python Connector for ETL/Data Pipeline.

읽기(SELECT) 전용 BigQuery Connector로 Pandas, Polars, PyArrow DataFrame을 지원합니다.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Iterator, Optional

import pandas as pd
from google.cloud import bigquery

if TYPE_CHECKING:
    import polars as pl
    import pyarrow as pa


class AuthMethod(Enum):
    """BigQuery 인증 방식."""

    SERVICE_ACCOUNT = "service_account"
    ADC = "application_default_credentials"


@dataclass
class BigQueryConfig:
    """BigQuery 연결 설정.

    Attributes:
        project_id: GCP 프로젝트 ID
        auth_method: 인증 방식 (SERVICE_ACCOUNT 또는 ADC)
        credentials_path: 서비스 계정 키 파일 경로 (SERVICE_ACCOUNT 방식 시 필수)
        location: BigQuery 리전 (기본값: asia-northeast3)
        timeout: 쿼리 타임아웃 초 (기본값: 300)
    """

    project_id: str
    auth_method: AuthMethod = AuthMethod.ADC
    credentials_path: Optional[str] = None
    location: str = "asia-northeast3"
    timeout: int = 300

    def __post_init__(self) -> None:
        """설정 유효성 검사."""
        if self.auth_method == AuthMethod.SERVICE_ACCOUNT:
            if not self.credentials_path:
                raise ValueError(
                    "credentials_path is required for SERVICE_ACCOUNT auth method"
                )
            if not os.path.exists(self.credentials_path):
                raise FileNotFoundError(
                    f"Credentials file not found: {self.credentials_path}"
                )

    @classmethod
    def from_env(cls) -> BigQueryConfig:
        """환경변수에서 설정 로드.

        환경변수:
            BIGQUERY_PROJECT_ID: GCP 프로젝트 ID (필수)
            BIGQUERY_AUTH_METHOD: 인증 방식 (service_account 또는 adc, 기본값: adc)
            BIGQUERY_CREDENTIALS_PATH: 서비스 계정 키 파일 경로
            BIGQUERY_LOCATION: BigQuery 리전 (기본값: asia-northeast3)
            BIGQUERY_TIMEOUT: 쿼리 타임아웃 초 (기본값: 300)
        """
        project_id = os.getenv("BIGQUERY_PROJECT_ID")
        if not project_id:
            raise ValueError("BIGQUERY_PROJECT_ID environment variable is required")

        auth_method_str = os.getenv("BIGQUERY_AUTH_METHOD", "adc").lower()
        auth_method = (
            AuthMethod.SERVICE_ACCOUNT
            if auth_method_str == "service_account"
            else AuthMethod.ADC
        )

        return cls(
            project_id=project_id,
            auth_method=auth_method,
            credentials_path=os.getenv("BIGQUERY_CREDENTIALS_PATH"),
            location=os.getenv("BIGQUERY_LOCATION", "asia-northeast3"),
            timeout=int(os.getenv("BIGQUERY_TIMEOUT", "300")),
        )

    def to_client_kwargs(self) -> dict:
        """BigQuery Client 생성에 필요한 kwargs 반환."""
        kwargs: dict = {
            "project": self.project_id,
            "location": self.location,
        }

        if self.auth_method == AuthMethod.SERVICE_ACCOUNT:
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
            kwargs["credentials"] = credentials

        return kwargs


class BigQueryConnector:
    """BigQuery 읽기 전용 Connector.

    ETL/데이터 파이프라인에서 데이터 읽기(SELECT)에 특화된 클래스입니다.

    Examples:
        # 기본 사용법
        config = BigQueryConfig(project_id="my-project")
        connector = BigQueryConnector(config)
        df = connector.to_pandas("SELECT * FROM dataset.table LIMIT 100")

        # Context manager 사용
        with BigQueryConnector.from_env() as connector:
            df = connector.to_pandas("SELECT * FROM dataset.table")
    """

    def __init__(self, config: BigQueryConfig) -> None:
        """BigQueryConnector 초기화.

        Args:
            config: BigQueryConfig 인스턴스
        """
        self.config = config
        self._client: Optional[bigquery.Client] = None

    @classmethod
    def from_env(cls) -> BigQueryConnector:
        """환경변수에서 설정을 로드하여 Connector 생성."""
        config = BigQueryConfig.from_env()
        return cls(config)

    @property
    def client(self) -> bigquery.Client:
        """Lazy initialization of BigQuery client."""
        if self._client is None:
            self._client = bigquery.Client(**self.config.to_client_kwargs())
        return self._client

    def execute(
        self, query: str, params: Optional[dict[str, str]] = None
    ) -> list[tuple]:
        """쿼리 실행 후 결과를 튜플 리스트로 반환.

        Args:
            query: 실행할 SQL 쿼리
            params: 쿼리 파라미터 (Named 파라미터 지원)

        Returns:
            쿼리 결과 행들의 튜플 리스트
        """
        job_config = bigquery.QueryJobConfig()

        if params:
            job_config.query_parameters = [
                bigquery.ScalarQueryParameter(key, "STRING", value)
                for key, value in params.items()
            ]

        query_job = self.client.query(
            query, job_config=job_config, timeout=self.config.timeout
        )

        results = query_job.result()
        return [tuple(row.values()) for row in results]

    def execute_iter(
        self,
        query: str,
        params: Optional[dict[str, str]] = None,
        page_size: int = 10000,
    ) -> Iterator[tuple]:
        """쿼리 실행 후 결과를 Iterator로 반환 (대용량 데이터용).

        Args:
            query: 실행할 SQL 쿼리
            params: 쿼리 파라미터
            page_size: 페이지 크기

        Yields:
            쿼리 결과 행 튜플
        """
        job_config = bigquery.QueryJobConfig()

        if params:
            job_config.query_parameters = [
                bigquery.ScalarQueryParameter(key, "STRING", value)
                for key, value in params.items()
            ]

        query_job = self.client.query(
            query, job_config=job_config, timeout=self.config.timeout
        )

        results = query_job.result(page_size=page_size)
        for row in results:
            yield tuple(row.values())

    def to_pandas(
        self,
        query: str,
        params: Optional[dict[str, str]] = None,
        use_bqstorage: bool = False,
    ) -> pd.DataFrame:
        """쿼리 실행 후 결과를 Pandas DataFrame으로 반환.

        Args:
            query: 실행할 SQL 쿼리
            params: 쿼리 파라미터
            use_bqstorage: BigQuery Storage API 사용 여부 (대용량 데이터 시 권장)

        Returns:
            Pandas DataFrame
        """
        job_config = bigquery.QueryJobConfig()

        if params:
            job_config.query_parameters = [
                bigquery.ScalarQueryParameter(key, "STRING", value)
                for key, value in params.items()
            ]

        query_job = self.client.query(
            query, job_config=job_config, timeout=self.config.timeout
        )

        if use_bqstorage:
            return query_job.result().to_dataframe(create_bqstorage_client=True)
        return query_job.result().to_dataframe()

    def to_polars(
        self,
        query: str,
        params: Optional[dict[str, str]] = None,
        use_bqstorage: bool = False,
    ) -> pl.DataFrame:
        """쿼리 실행 후 결과를 Polars DataFrame으로 반환.

        Args:
            query: 실행할 SQL 쿼리
            params: 쿼리 파라미터
            use_bqstorage: BigQuery Storage API 사용 여부

        Returns:
            Polars DataFrame
        """
        import polars as pl

        pandas_df = self.to_pandas(query, params, use_bqstorage)
        return pl.from_pandas(pandas_df)

    def to_arrow(
        self, query: str, params: Optional[dict[str, str]] = None
    ) -> pa.Table:
        """쿼리 실행 후 결과를 PyArrow Table로 반환.

        Args:
            query: 실행할 SQL 쿼리
            params: 쿼리 파라미터

        Returns:
            PyArrow Table
        """
        job_config = bigquery.QueryJobConfig()

        if params:
            job_config.query_parameters = [
                bigquery.ScalarQueryParameter(key, "STRING", value)
                for key, value in params.items()
            ]

        query_job = self.client.query(
            query, job_config=job_config, timeout=self.config.timeout
        )

        return query_job.result().to_arrow()

    def get_schema(self, table_id: str) -> list[bigquery.SchemaField]:
        """테이블 스키마 조회.

        Args:
            table_id: 테이블 ID (dataset.table 또는 project.dataset.table)

        Returns:
            SchemaField 리스트
        """
        table = self.client.get_table(table_id)
        return list(table.schema)

    def list_datasets(self) -> list[str]:
        """프로젝트 내 데이터셋 목록 조회."""
        return [dataset.dataset_id for dataset in self.client.list_datasets()]

    def list_tables(self, dataset_id: str) -> list[str]:
        """데이터셋 내 테이블 목록 조회.

        Args:
            dataset_id: 데이터셋 ID

        Returns:
            테이블 ID 리스트
        """
        tables = self.client.list_tables(dataset_id)
        return [table.table_id for table in tables]

    def dry_run(self, query: str) -> dict:
        """쿼리 Dry Run (실제 실행 없이 검증 및 비용 추정).

        Args:
            query: 검증할 SQL 쿼리

        Returns:
            dict with 'valid', 'bytes_processed', 'estimated_cost_usd'
        """
        job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

        try:
            query_job = self.client.query(query, job_config=job_config)
            bytes_processed = query_job.total_bytes_processed
            # BigQuery 가격: $5 per TB (on-demand pricing)
            estimated_cost = (bytes_processed / (1024**4)) * 5

            return {
                "valid": True,
                "bytes_processed": bytes_processed,
                "bytes_processed_human": self._format_bytes(bytes_processed),
                "estimated_cost_usd": round(estimated_cost, 4),
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
            }

    @staticmethod
    def _format_bytes(bytes_value: int) -> str:
        """바이트를 사람이 읽기 쉬운 형태로 변환."""
        value = float(bytes_value)
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if value < 1024:
                return f"{value:.2f} {unit}"
            value /= 1024
        return f"{value:.2f} PB"

    def close(self) -> None:
        """클라이언트 연결 종료."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> BigQueryConnector:
        """Context manager 진입."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager 종료."""
        self.close()
