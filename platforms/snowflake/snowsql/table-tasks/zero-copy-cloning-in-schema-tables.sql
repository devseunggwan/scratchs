-- 변수 설정
SET src_db = '';
SET src_schema = '';
SET tgt_db = '';
SET tgt_schema = '';

-- 소스 스키마에서 테이블 목록을 가져오기
CREATE OR REPLACE TABLE tables_to_clone AS
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_CATALOG = $src_db AND TABLE_SCHEMA = $src_schema;

-- 모든 테이블을 복제하는 스크립트 생성
DECLARE
  tables CURSOR FOR
    SELECT TABLE_NAME
    FROM tables_to_clone;
  table_name STRING;
  clone_stmt STRING;
BEGIN
  FOR table_record IN tables DO
    table_name := table_record.TABLE_NAME;
    clone_stmt := 'CREATE TABLE ' || $tgt_db || '.' || $tgt_schema || '.' || table_name || ' CLONE ' || $src_db || '.' || $src_schema || '.' || table_name || ';';
    EXECUTE IMMEDIATE clone_stmt;
  END FOR;
END;

-- 임시 테이블 정리
DROP TABLE tables_to_clone;
