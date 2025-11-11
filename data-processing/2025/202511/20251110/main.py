import os

import pandas as pd
from dotenv import load_dotenv
from infrastructure.adapter.trino import TrinoAdapter

if __name__ == "__main__":
    load_dotenv()
    trino_prod_adapter = TrinoAdapter(
        host=os.getenv("PROD__TRINO_HOST"),
        port=os.getenv("PROD__TRINO_PORT"),
        user=os.getenv("PROD__TRINO_USER"),
    )
    trino_dev_adapter = TrinoAdapter(
        host=os.getenv("DEV__TRINO_HOST"),
        port=os.getenv("DEV__TRINO_PORT"),
        user=os.getenv("DEV__TRINO_USER")
    )
    
    query_1 = """
    """
    
    query_2 = """
    """

    df_1 = trino_prod_adapter.to_pandas(query_1)
    df_2 = trino_dev_adapter.to_pandas(query_2)
    
    df = pd.merge(
        df_1, 
        df_2, 
        on=[],
        how="left",
        suffixes=("_prod", "_dev")
    )
    
    print(f"Merge 결과: {len(df):,} 행")
    
    # Merge된 DataFrame에서 값 비교
    print("\n" + "="*80)
    print("Merge된 DataFrame 컬럼 값 비교 결과")
    print("="*80)
    
    # _prod와 _dev suffix를 가진 컬럼 쌍 찾기
    prod_cols = [col for col in df.columns if col.endswith("_prod")]
    dev_cols = [col for col in df.columns if col.endswith("_dev")]
    
    # 컬럼명 기준으로 쌍 매칭
    column_pairs = []
    for prod_col in prod_cols:
        base_name = prod_col[:-5]  # "_prod" 제거
        dev_col = base_name + "_dev"
        if dev_col in dev_cols:
            column_pairs.append((base_name, prod_col, dev_col))
    
    print(f"\n[비교 대상 컬럼]")
    print(f"총 {len(column_pairs)}개의 컬럼 쌍을 비교합니다.")
    
    if not column_pairs:
        print("⊗ 비교할 컬럼 쌍이 없습니다.")
    else:
        # 각 컬럼 쌍에 대해 값 비교
        print(f"\n[컬럼별 값 비교]")
        
        all_match = True
        diff_details = []
        
        for base_name, prod_col, dev_col in column_pairs:
            # 두 컬럼의 데이터 타입 확인
            prod_dtype = df[prod_col].dtype
            dev_dtype = df[dev_col].dtype
            
            # NaN을 포함한 값 비교
            is_equal = (df[prod_col] == df[dev_col]) | (df[prod_col].isna() & df[dev_col].isna())
            diff_count = (~is_equal).sum()
            
            if diff_count > 0:
                all_match = False
                # 차이가 있는 행의 인덱스
                diff_indices = df[~is_equal].index.tolist()
                
                # 샘플 데이터 (최대 3개)
                sample_size = min(3, diff_count)
                sample_diff = df.loc[diff_indices[:sample_size], 
                                    ["ad_datetime_id", "campaign_id", "adset_id", "ad_id", "keyword_id",
                                     prod_col, dev_col]]
                
                diff_details.append({
                    "column": base_name,
                    "count": diff_count,
                    "prod_dtype": prod_dtype,
                    "dev_dtype": dev_dtype,
                    "sample": sample_diff
                })
        
        if all_match:
            print("✓ 모든 컬럼의 값이 완전히 일치합니다!")
        else:
            print(f"✗ {len(diff_details)}개 컬럼에서 차이가 발견되었습니다.\n")
            
            for detail in diff_details:
                print(f"컬럼: {detail['column']}")
                print(f"  - 차이 발견 행 수: {detail['count']:,}개")
                print(f"  - 데이터 타입: prod({detail['prod_dtype']}) vs dev({detail['dev_dtype']})")
                print(f"  - 샘플 데이터 (최대 3개):")
                print(detail['sample'].to_string(index=False))
                print()
        
        # 통계 요약
        print(f"\n[요약]")
        print(f"  - 전체 행 수: {len(df):,}")
        print(f"  - 비교한 컬럼 수: {len(column_pairs)}")
        print(f"  - 차이가 있는 컬럼 수: {len(diff_details)}")
        print(f"  - 일치하는 컬럼 수: {len(column_pairs) - len(diff_details)}")
    
    print("\n" + "="*80)