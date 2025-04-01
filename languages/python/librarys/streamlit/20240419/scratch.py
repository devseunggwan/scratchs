import datetime
import streamlit as st

today = datetime.datetime.now() - datetime.timedelta(days=1)
last_week = today - datetime.timedelta(days=7)

with st.sidebar:
    option = st.selectbox("기간 선택 방식", ("기간 선택", "달력 선택"))

    if option == "기간 선택":
        end_date = st.date_input(
            "기준 일자를 선택하세요",
            today,
            format="YYYY.MM.DD",
            max_value=today,
        )
        period = st.radio(
            "비교할 기간을 선택하세요.",
            [1, 7, 14, 18, 30, 60, 90, 180, 365],
            index=1,
        )
        start_date = (end_date - datetime.timedelta(days=period)).strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        st.write(f"기간: {start_date} ~ {end_date}")
    else:
        period = st.date_input(
            "비교할 기간을 선택하세요.",
            (last_week, today),
            format="YYYY.MM.DD",
            max_value=today,
        )

        start_date = period[0].strftime("%Y-%m-%d")
        end_date = (
            period[1].strftime("%Y-%m-%d")
            if len(period) > 1
            else today.strftime("%Y-%m-%d")
        )
