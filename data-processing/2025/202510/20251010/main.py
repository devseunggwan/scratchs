import json
import io
from typing import List, Dict, Any

import boto3  # AWS SDK for S3 접근
import polars as pl


def read_manifest_json(file_path: str) -> Dict[str, Any]:
    """
    manifest.json 파일을 읽어서 파이썬 딕셔너리로 반환

    Args:
        file_path (str): manifest.json 파일 경로

    Returns:
        Dict[str, Any]: 매니페스트 데이터
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
        return manifest_data
    except FileNotFoundError:
        raise FileNotFoundError(f"manifest.json 파일을 찾을 수 없습니다: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"manifest.json 파일을 파싱할 수 없습니다: {e}")


def get_s3_file_paths(manifest_data: Dict[str, Any], source_bucket: str) -> List[str]:
    """
    매니페스트 데이터에서 S3 파일 경로들을 추출

    Args:
        manifest_data (Dict[str, Any]): 매니페스트 데이터
        source_bucket (str): 소스 버킷 이름

    Returns:
        List[str]: S3 파일 경로 리스트
    """
    s3_paths = []
    for file_info in manifest_data.get('files', []):
        key = file_info.get('key')
        if key:
            # S3 경로 구성 (s3://bucket/key 형식)
            s3_path = f"s3://{source_bucket}/{key}"
            s3_paths.append(s3_path)

    return s3_paths


def read_parquet_from_s3(s3_paths: List[str]) -> pl.DataFrame:
    """
    S3에서 Parquet 파일들을 읽어서 단일 polars DataFrame으로 반환

    Args:
        s3_paths (List[str]): S3 파일 경로 리스트

    Returns:
        pl.DataFrame: 결합된 데이터프레임
    """
    if not s3_paths:
        print("경고: 처리할 파일이 없습니다.")
        return pl.DataFrame()

    # S3 클라이언트 설정
    s3_client = boto3.client('s3')

    dataframes = []

    for i, s3_path in enumerate(s3_paths, 1):
        try:
            print(f"파일 {i}/{len(s3_paths)} 처리 중: {s3_path}")

            # S3 경로 파싱 (s3://bucket/key 형식)
            if not s3_path.startswith('s3://'):
                raise ValueError(f"잘못된 S3 경로 형식: {s3_path}")

            path_part = s3_path[5:]  # 's3://' 제거
            bucket, key = path_part.split('/', 1)

            # S3에서 파일을 바이너리로 읽기
            response = s3_client.get_object(Bucket=bucket, Key=key)
            parquet_data = response['Body'].read()

            # BytesIO를 사용해서 polars로 Parquet 파일 읽기
            parquet_buffer = io.BytesIO(parquet_data)
            df = pl.read_parquet(parquet_buffer)

            dataframes.append(df)
            print(f"성공: {len(df)} 행 읽음")

        except Exception as e:
            print(f"오류 발생 - {s3_path}: {e}")
            continue

    if not dataframes:
        raise ValueError("읽을 수 있는 Parquet 파일이 없습니다.")

    # 모든 데이터프레임을 결합
    combined_df = pl.concat(dataframes, how="vertical")

    return combined_df


def save_to_local_parquet(df: pl.DataFrame, output_path: str) -> None:
    """
    데이터프레임을 로컬 Parquet 파일로 저장

    Args:
        df (pl.DataFrame): 저장할 데이터프레임
        output_path (str): 출력 파일 경로
    """
    df.write_parquet(output_path)
    print(f"데이터프레임이 {output_path}에 저장되었습니다.")


def main():
    """
    메인 함수: manifest.json을 읽어서 S3 Parquet 파일들을 처리
    """
    # manifest.json 파일 경로 (현재 디렉토리 기준)
    manifest_path = "manifest.json"

    try:
        # 1. 매니페스트 파일 읽기
        print("매니페스트 파일 읽는 중...")
        manifest_data = read_manifest_json(manifest_path)

        # 2. S3 파일 경로 추출
        source_bucket = manifest_data.get('destinationBucket', '')
        if not source_bucket:
            raise ValueError("매니페스트에서 sourceBucket 정보를 찾을 수 없습니다.")

        print(f"소스 버킷: {source_bucket}")
        print(f"파일 개수: {len(manifest_data.get('files', []))} 개")

        s3_paths = get_s3_file_paths(manifest_data, source_bucket)

        # 3. S3에서 Parquet 파일들 읽기
        print("S3에서 Parquet 파일들 읽는 중...")
        combined_df = read_parquet_from_s3(s3_paths)

        # 4. 결과 정보 출력
        print("=== 처리 결과 ===")
        print(f"총 읽은 행 수: {len(combined_df)}")
        print(f"컬럼 수: {len(combined_df.columns)}")
        print(f"컬럼 이름: {combined_df.columns}")

        # 5. 데이터프레임 샘플 출력 (처음 5행)
        print("\n=== 데이터 샘플 ===")
        print(combined_df.head())

        save_to_local_parquet(combined_df, "./output/combined_output.parquet")

    except Exception as e:
        print(f"오류 발생: {e}")
        return None


if __name__ == "__main__":
    main()
