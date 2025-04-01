import os

import pandas as pd
import snowflake.snowpark as snowpark
import snowflake.snowpark.types as T
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from pygwalker.api.streamlit import get_streamlit_html, init_streamlit_comm
from snowflake.snowpark import Session
from streamlit_ydata_profiling import st_profile_report
from ydata_profiling import ProfileReport


def describe_snowpark_df(snowpark_df: snowpark.DataFrame):
    st.write("업로드한 테이블의 정보입니다.")
    numeric_types = [
        T.DecimalType,
        T.LongType,
        T.DoubleType,
        T.FloatType,
        T.IntegerType,
    ]
    numeric_columns = [
        c.name for c in snowpark_df.schema.fields if type(c.datatype) in numeric_types
    ]

    # Get categorical columns
    categorical_types = [T.StringType]
    categorical_columns = [
        c.name
        for c in snowpark_df.schema.fields
        if type(c.datatype) in categorical_types
    ]

    st.write("Relational schema:")

    columns = [c for c in snowpark_df.schema.fields]
    st.write(columns)

    col1, col2 = st.columns(2)
    with col1:
        st.write("Numeric columns:\t", numeric_columns)

    with col2:
        st.write("Categorical columns:\t", categorical_columns)

    # Calculte statistics for our dataset
    st.dataframe(snowpark_df.describe().sort("SUMMARY"), use_container_width=True)


def load_infer_and_persist(file) -> snowpark.DataFrame:
    file_df = pd.read_csv(file)
    snowparkDf = session.write_pandas(
        file_df, file.name, auto_create_table=True, overwrite=True
    )
    return snowparkDf


# When using `use_kernel_calc=True`, you should cache your pygwalker html, if you don't want your memory to explode
@st.cache_resource
def get_pyg_html(df: pd.DataFrame) -> str:
    html = get_streamlit_html(df, spec="./gw0.json", use_kernel_calc=True)
    return html


if __name__ == "__main__":
    load_dotenv()

    # connect to Snowflake
    connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "role": os.getenv("SNOWFLAKE_ROLE"),  # optional
        "warehouse": os.getenv("SNOWFLAKE_WH"),  # optional
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    }
    session = Session.builder.configs(connection_parameters).create()

    st.set_page_config(
        page_title="Snowflake data uploader", page_icon="❄️", layout="wide"
    )

    st.header("❄️ Snowflake data uploader")

    file = st.file_uploader("Drop your CSV here", type={"csv"})

    if file is not None:
        df = load_infer_and_persist(file)
        st.subheader("Great, your data has been uploaded to Snowflake!")

        with st.status("테이블 제원 정보"):
            describe_snowpark_df(df)
            st.write("Data loaded to Snowflake:")
            st.dataframe(df)

        with st.status("테이블 기초 분석", expanded=False):
            report = ProfileReport(df.to_pandas(), orange_mode=True, explorative=True)
            st_profile_report(report, navbar=True)

        st.subheader("테이블 직접 분석")
        # Initialize pygwalker communication
        init_streamlit_comm()
        components.html(
            get_pyg_html(df.to_pandas()), width=1900, height=1000, scrolling=True
        )
