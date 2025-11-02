# S3 Parquet 파일 처리 프로젝트 (boto3 버전)

이 프로젝트는 manifest.json 파일을 읽어서 S3에 저장된 Parquet 파일들을 boto3와 polars를 사용하여 DataFrame으로 변환하는 기능을 제공합니다.

## 기능

- `manifest.json` 파일을 파싱하여 S3 파일 정보 추출
- boto3를 사용해 S3에서 Parquet 파일들을 읽어서 단일 polars DataFrame으로 결합
- 오류 처리 및 진행 상황 로깅
- 결과 데이터프레임 정보 출력

## 설치 방법

필요한 패키지를 설치하세요:

```bash
pip install -r requirements.txt
```

또는 conda를 사용하세요:

```bash
conda install -c conda-forge polars boto3
```

## 사용 방법

### 기본 실행

```python
python main.py
```

### 주요 함수들

#### `read_manifest_json(file_path: str) -> Dict[str, Any]`
manifest.json 파일을 읽어서 파이썬 딕셔너리로 반환합니다.

#### `get_s3_file_paths(manifest_data: Dict[str, Any], source_bucket: str) -> List[str]`
매니페스트 데이터에서 S3 파일 경로들을 추출합니다.

#### `read_parquet_from_s3(s3_paths: List[str]) -> pl.DataFrame`
boto3를 사용해 S3에서 Parquet 파일들을 읽어서 단일 polars DataFrame으로 반환합니다.

## 구현 방식

이번 버전에서는 다음과 같은 방식으로 구현되었습니다:

1. **boto3 클라이언트 사용**: S3 접근을 위해 boto3.client('s3') 사용
2. **바이너리 데이터 처리**: S3 객체를 바이너리로 읽어온 후 BytesIO를 사용
3. **메모리 효율성**: 스트리밍 방식이 아닌 파일 전체를 메모리에 로드

## manifest.json 파일 구조

```json
{
  "sourceBucket": "버킷-이름",
  "destinationBucket": "대상-버킷",
  "version": "버전",
  "creationTimestamp": "타임스탬프",
  "fileFormat": "Parquet",
  "fileSchema": "스키마-정의",
  "files": [
    {
      "key": "파일-경로/파일명.parquet",
      "size": 파일크기,
      "MD5checksum": "체크섬"
    }
  ]
}
```

## 출력 예시

```
매니페스트 파일 읽는 중...
소스 버킷: laplace-airflow
파일 개수: 30 개
S3에서 Parquet 파일들 읽는 중...
파일 1/30 처리 중: s3://laplace-airflow/logs-kubernetes-provider/parquet/...

=== 처리 결과 ===
총 읽은 행 수: 123456
컬럼 수: 10
컬럼 이름: ['컬럼1', '컬럼2', ...]

=== 데이터 샘플 ===
shape: (5, 10)
┌─────────┬─────────┬─────────┬─────────┬─────────┐
│ 컬럼1   │ 컬럼2   │ 컬럼3   │ ...     │ 컬럼10  │
│ ---     │ ---     │ ---     │ ---     │ ---     │
│ str     │ str     │ i64     │ ...     │ str     │
╞═════════╪═════════╪═════════╪═════════╪═════════╡
│ 데이터1 │ 데이터2 │ 123     │ ...     │ 데이터10│
│ 데이터1 │ 데이터2 │ 456     │ ...     │ 데이터10│
│ ...     │ ...     │ ...     │ ...     │ ...     │
└─────────┴─────────┴─────────┴─────────┴─────────┘
```

## 오류 처리

- 파일이 존재하지 않거나 파싱할 수 없는 경우 적절한 오류 메시지를 출력합니다.
- 개별 Parquet 파일 읽기 실패 시 건너뛰고 다음 파일을 처리합니다.
- 모든 파일 읽기에 실패한 경우 적절한 오류를 발생시킵니다.
- S3 접근 권한 오류 시 boto3에서 적절한 예외가 발생합니다.

## 주의사항

- AWS 자격 증명 설정이 필요합니다 (환경변수, IAM 역할, 또는 AWS CLI 설정)
- S3 버킷에 대한 읽기 권한이 필요합니다
- 대용량 파일들의 경우 메모리 사용량에 주의하세요 (파일 전체를 메모리에 로드)
- 네트워크 타임아웃 설정을 고려해야 할 수 있습니다