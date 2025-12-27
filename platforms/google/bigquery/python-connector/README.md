# BigQuery Python Connector

ETL/데이터 파이프라인을 위한 BigQuery 읽기 전용 Python Connector입니다.

## Features

- 읽기(SELECT) 전용 설계
- Pandas, Polars, PyArrow DataFrame 지원
- 서비스 계정 키 파일 및 ADC 인증 지원
- 쿼리 Dry Run 및 비용 추정
- Context Manager 지원
- 대용량 데이터 처리를 위한 Iterator 지원

## Installation

```bash
# pip 사용
pip install -e .

# 선택적 의존성 포함 (Polars, BigQuery Storage API)
pip install -e ".[all]"

# 개발 의존성 포함
pip install -e ".[dev]"
```

## Quick Start

### 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일 편집:

```bash
BIGQUERY_PROJECT_ID=your-gcp-project-id
BIGQUERY_AUTH_METHOD=adc
BIGQUERY_LOCATION=asia-northeast3
```

### 기본 사용법

```python
from dotenv import load_dotenv
load_dotenv()

from connector import BigQueryConnector

with BigQueryConnector.from_env() as connector:
    # Pandas DataFrame
    df = connector.to_pandas("SELECT * FROM dataset.table LIMIT 100")
    print(df)
```

### Polars DataFrame

```python
with BigQueryConnector.from_env() as connector:
    df_pl = connector.to_polars("SELECT * FROM dataset.table LIMIT 100")
    print(df_pl)
```

### 쿼리 비용 추정

```python
with BigQueryConnector.from_env() as connector:
    result = connector.dry_run("SELECT * FROM dataset.large_table")
    print(f"처리할 데이터: {result['bytes_processed_human']}")
    print(f"예상 비용: ${result['estimated_cost_usd']}")
```

## Authentication

### 1. ADC (Application Default Credentials) - 기본값

로컬 개발 환경:

```bash
gcloud auth application-default login
```

GCE, Cloud Run, GKE 등 GCP 환경에서는 자동으로 메타데이터 서버에서 인증 정보를 획득합니다.

### 2. 서비스 계정 키 파일

`.env` 설정:

```bash
BIGQUERY_PROJECT_ID=your-gcp-project-id
BIGQUERY_AUTH_METHOD=service_account
BIGQUERY_CREDENTIALS_PATH=/path/to/credentials.json
```

또는 직접 설정:

```python
from connector import AuthMethod, BigQueryConfig, BigQueryConnector

config = BigQueryConfig(
    project_id="my-gcp-project",
    auth_method=AuthMethod.SERVICE_ACCOUNT,
    credentials_path="./credentials.json",
)

with BigQueryConnector(config) as connector:
    df = connector.to_pandas("SELECT 1")
```

## API Reference

### BigQueryConfig

| 속성 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `project_id` | `str` | 필수 | GCP 프로젝트 ID |
| `auth_method` | `AuthMethod` | `ADC` | 인증 방식 |
| `credentials_path` | `str` | `None` | 서비스 계정 키 파일 경로 |
| `location` | `str` | `asia-northeast3` | BigQuery 리전 |
| `timeout` | `int` | `300` | 쿼리 타임아웃 (초) |

### BigQueryConnector Methods

| 메서드 | 반환 타입 | 설명 |
|--------|----------|------|
| `execute(query, params)` | `list[tuple]` | 쿼리 실행, 튜플 리스트 반환 |
| `execute_iter(query, params, page_size)` | `Iterator[tuple]` | 대용량 데이터용 Iterator |
| `to_pandas(query, params, use_bqstorage)` | `pd.DataFrame` | Pandas DataFrame 반환 |
| `to_polars(query, params, use_bqstorage)` | `pl.DataFrame` | Polars DataFrame 반환 |
| `to_arrow(query, params)` | `pa.Table` | PyArrow Table 반환 |
| `dry_run(query)` | `dict` | 쿼리 검증 및 비용 추정 |
| `get_schema(table_id)` | `list[SchemaField]` | 테이블 스키마 조회 |
| `list_datasets()` | `list[str]` | 데이터셋 목록 조회 |
| `list_tables(dataset_id)` | `list[str]` | 테이블 목록 조회 |

## Examples

### 파라미터 쿼리

```python
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
```

### 대용량 데이터 처리

```python
with BigQueryConnector.from_env() as connector:
    # Iterator 사용 (메모리 효율적)
    for row in connector.execute_iter(
        "SELECT * FROM dataset.large_table",
        page_size=10000,
    ):
        process(row)

    # BigQuery Storage API 사용 (더 빠름)
    df = connector.to_pandas(
        "SELECT * FROM dataset.large_table",
        use_bqstorage=True,
    )
```

### 스키마 및 메타데이터 조회

```python
with BigQueryConnector.from_env() as connector:
    # 데이터셋 목록
    datasets = connector.list_datasets()

    # 테이블 목록
    tables = connector.list_tables("my_dataset")

    # 테이블 스키마
    schema = connector.get_schema("my_dataset.my_table")
    for field in schema:
        print(f"{field.name}: {field.field_type}")
```

## Environment Variables

| 변수 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `BIGQUERY_PROJECT_ID` | O | - | GCP 프로젝트 ID |
| `BIGQUERY_AUTH_METHOD` | X | `adc` | 인증 방식 (`adc` 또는 `service_account`) |
| `BIGQUERY_CREDENTIALS_PATH` | △ | - | 서비스 계정 키 파일 경로 |
| `BIGQUERY_LOCATION` | X | `asia-northeast3` | BigQuery 리전 |
| `BIGQUERY_TIMEOUT` | X | `300` | 쿼리 타임아웃 (초) |

△: `BIGQUERY_AUTH_METHOD=service_account`인 경우 필수

## Dependencies

### Required

- `google-cloud-bigquery>=3.25.0`
- `pandas>=2.0.0`
- `pyarrow>=15.0.0`
- `python-dotenv>=1.0.0`

### Optional

- `polars>=1.0.0` - Polars DataFrame 지원
- `google-cloud-bigquery-storage>=2.25.0` - BigQuery Storage API (대용량 데이터 성능 향상)
