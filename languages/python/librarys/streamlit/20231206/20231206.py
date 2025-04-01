import pandas as pd
import streamlit as st

df = pd.read_csv("./data/table2.csv")


def get_delta(metric: str, today: pd.Series, before: pd.Series):
    return round((today[metric] - before[metric]) / before[metric] * 100, 2)


if __name__ == "__main__":
    period = 90

    today = df.iloc[0]
    before = df.iloc[period - 1]

    st.set_page_config(layout="wide")
    
    with st.sidebar:
        st.title("NFTtown Dashboard")

        period = st.slider(label="기간", min_value=10, max_value=180, value=90, step=10)
        before = df.iloc[period - 1]

    st.header("Daily Stats")
    col11, col12, col13, col14 = st.columns(4)
    col11.metric(
        label="누적 신규 방문자수(12.15~)",
        value=today["vistors"],
        delta=get_delta("vistors", today, before),
    )
    col12.metric(label="MAU", value=today["MAU"], delta=get_delta("MAU", today, before))
    col13.metric(
        label="SNS 총 팔로워수",
        value=today["sns_followers_all"],
        delta=get_delta("sns_followers_all", today, before),
    )
    col14.metric(
        label="NFTtown 가입자수",
        value=today["accounters_all"],
        delta=get_delta("accounters_all", today, before),
    )

    col21, col22, col23, col24 = st.columns(4)
    col21.metric(
        label="신규 방문자수",
        value=today["new_inventor"],
        delta=get_delta("new_inventor", today, before),
    )
    col22.metric(label="DAU", value=today["MAU"], delta=get_delta("DAU", today, before))
    col23.metric(label="WAU", value=today["WAU"], delta=get_delta("WAU", today, before))
    col24.metric(
        label="재방문율(WAU/MAU)",
        value=today["WAU/MAU"],
        delta=get_delta("WAU/MAU", today, before),
    )

    col31, col32, col33, col34 = st.columns(4)
    col31.metric(
        label="트위터 팔로워수",
        value=today["twitter_followers"],
        delta=get_delta("twitter_followers", today, before),
    )
    col32.metric(
        label="디스코드 맴버수",
        value=today["discord_members"],
        delta=get_delta("discord_members", today, before),
    )
    col33.metric(
        label="Brezel 지갑연결수",
        value=today["brezel"],
        delta=get_delta("brezel", today, before),
    )
    col34.metric(
        label="유튜브 팔로워",
        value=today["youtube_followers"],
        delta=get_delta("youtube_followers", today, before),
    )
    
    # tab1, tab2, tab3 = st.tabs(["Daily Active Users", "Daily Followers", "Daily Accounts"])

    chart1, chart2, chart3 = st.columns(3)
    
    with chart1:
        st.header("Daily Active Users")
        st.line_chart(
            df.iloc[0:period],
            x="date",
            y=["MAU", "DAU", "WAU", "WAU/MAU", "new_inventor"],
            height=500,
        )

    with chart2:
        st.header("Daily Followers")
        st.line_chart(
            df.iloc[0:period],
            x="date",
            y=[
                "twitter_followers",
                "discord_members",
                "youtube_followers",
                "sns_followers_all",
            ],
            height=500,
        )

    with chart3:
        st.header("Daily Accounts")
        st.line_chart(
            df.iloc[0:period],
            x="date",
            y=["new_accounters", "accounters_all", "brezel_all", "brezel"],
            height=500,
        )

    st.header("Data Source")
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False),
        file_name="nfttown.csv",
        mime="text/csv",
    )
    st.write(df)
