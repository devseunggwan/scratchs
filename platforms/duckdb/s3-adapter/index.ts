import { DuckDBConnection } from "@duckdb/node-api";

class DuckDBAdapter {
  private connection: DuckDBConnection | null;

  constructor() {
    this.connection = null;
  }

  async s3Initialize() {
    this.connection = await DuckDBConnection.create();

    // S3 인증 설정
    await this.connection.run(`
        CREATE OR REPLACE SECRET s3_secret (
          TYPE s3,
          PROVIDER credential_chain,
          REGION 'ap-northeast-2'
        )
      `);

    // 성능 최적화 설정
    await this.connection.run("SET memory_limit = '8GB'");
    await this.connection.run("SET threads = 12");
    await this.connection.run("SET preserve_insertion_order = false");
  }

  async query(query: string) {
    if (!this.connection) {
      throw new Error("Connection not initialized. Call s3Initialize() first.");
    }
    return await this.connection.runAndReadAll(query);
  }

  disconnect() {
    if (this.connection) {
      this.connection.disconnectSync();
    }
  }
}

async function main() {
  const adapter = new DuckDBAdapter();
  const query = `
    SELECT data.id
      FROM read_ndjson_auto('s3://test-bucket/date_id=*/*.ndjson.gz', hive_partitioning=true)
  `;

  try {
    await adapter.s3Initialize();
    const result = await adapter.query(query);

    if (result && "getRowObjectsJson" in result) {
      const resultJson = result.getRowObjectsJson();
      console.log(resultJson);
    }
  } catch (error) {
    console.error("Error:", error);
  } finally {
    // 연결을 정리합니다
    adapter.disconnect();
  }
}

// 메인 함수를 실행합니다
main().catch(console.error);
