import json
import os

import duckdb
from dotenv import load_dotenv
from modules.sf_connector import SfConnector
from modules.sf_cortex_llm import SfCortexLLM
from tqdm import tqdm

load_dotenv(dotenv_path=".env", verbose=True, override=True)

connector = SfConnector(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    role=os.getenv("SNOWFLAKE_ROLE"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)


if __name__ == "__main__":
    session = next(connector.get_session())

    df = duckdb.read_csv(
        ["./data/voc-test-sample.csv", "./data/voc-test-sample-2nd.csv"],
        header=True,
        delimiter=",",
        quotechar='"',
    ).to_df()
    df = df.replace('"', "", regex=True)

    model_name = "mistral-large"
    model_options = {"temperature": 0.0, "max_tokens": 2000}

    cortex = SfCortexLLM(
        session=session, model_name=model_name, model_options=model_options
    )

    results = []
    for item in tqdm(df[["file_name", "text"]].values.tolist()):
        item = [x.replace('"', "") for x in item]
        file_name, text = item

        result = {"file_name": file_name, "original_text": text}
        result = result | cortex.run(text)

        results.append(result)

    results = {"data": results}

    with open("./data/results.json", "w") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
