import duckdb

if __name__ == "__main__":
    query = """
        SELECT 
            *
        FROM 
            read_json_auto('s3://scratchs-bucket/_tmp/**/_compacted/*.json.gz')
    """

    conn = duckdb.connect()
    conn.execute("""
        INSTALL httpfs;
        LOAD 'httpfs';
    """)

    # 데이터 쿼리
    df = conn.execute(query).df().to_csv("output.csv", index=False)
    print(df)
