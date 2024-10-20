import logging
import os
import time
from datetime import datetime

import httpx
import openai
import pandas as pd
import streamlit as st
from service import NftCurationLLM
from streamlit_image_select import image_select


class NftCurationUI:
    def __init__(self, llm: NftCurationLLM):
        self.llm_instance = llm

        self.models = ["gpt-4o", "gpt-4-turbo"]
        self.model = "gpt-4o"

        self.headers = {"x-api-key": os.getenv("RESERVOIR_API_KEY")}
        self.reservoir_networks_url_prefix = {
            "ethereum": "api",
            "polygon": "api-polygon",
            "bsc": "api-bsc",
            "arbitrum": "api-arbitrum",
            "optimism": "api-optimism",
            "base": "api-base",
            "linea": "api-linea",
            "avalanche": "api-avalanche",
        }
        self.reservoir_period = ["1d", "7d", "30d"]
        self.reservoir_ranking_url = (
            lambda x: f"https://{self.reservoir_networks_url_prefix[x]}.reservoir.tools/collections/trending/v1"
        )
        self.reservoir_collection_url = (
            lambda x: f"https://{self.reservoir_networks_url_prefix[x]}.reservoir.tools/collections/v7"
        )
        self.reservoir_nft_list_url = (
            lambda x: f"https://{self.reservoir_networks_url_prefix[x]}.reservoir.tools/tokens/v7"
        )

        self.logger = logging.getLogger(st.__name__)

    @st.cache_data(ttl="1h", hash_funcs={httpx.Client: id})
    def get_collection_ranking(
        _self, network, period: str = "1d", sortby: str = "volume"
    ):
        params = {
            "period": period,
            "sortBy": sortby,
            "limit": 100,
        }
        __url = _self.reservoir_ranking_url(network)

        ranking = httpx.get(__url, params=params, headers=_self.headers).json()

        return ranking

    def st_sidebar(self):
        with st.sidebar:
            st.header("NFT Curation Bot")

            network = st.selectbox(
                "Network", list(self.reservoir_networks_url_prefix.keys())
            )
            collection_id = st.text_input("Collection ID")

            with st.expander("LLM Model Options"):
                self.model = st.selectbox("Model", self.models)
                self.nft_image_counts = st.slider("NFT Images", 1, 20, 10, 1)
                self.max_tokens = st.slider("Max Tokens", 50, 1000, 500, 50)
                self.question_count = st.slider("Question Count", 1, 3, 1, 1)
            with st.expander("Prompt - NFT 설명"):
                self.llm_instance.prompt_description = st.text_area(
                    "Prompt Description",
                    self.llm_instance.prompt_description,
                    height=500,
                    label_visibility="collapsed",
                )
            with st.expander("Prompt - NFT 태그"):
                self.llm_instance.prompt_tag = st.text_area(
                    "Prompt Tag",
                    self.llm_instance.prompt_tag,
                    height=500,
                    label_visibility="collapsed",
                )
            with st.expander("Prompt - NFT 한줄 요약"):
                self.llm_instance.prompt_curation = st.text_area(
                    "Prompt Curation",
                    self.llm_instance.prompt_curation,
                    height=500,
                    label_visibility="collapsed",
                )

            is_click = st.button("Run")

            return network, collection_id, is_click

    def st_ranking(self):
        st.header("Collection Ranking")

        col_network, col_period, col_sortby = st.columns(3)
        with col_network:
            ranking_network = st.selectbox(
                "Select Network", list(self.reservoir_networks_url_prefix.keys())
            )

        with col_period:
            period = st.selectbox("Period", self.reservoir_period)
        with col_sortby:
            sortby = st.selectbox("Sort By", ["volume", "sales"])

        ranking = self.get_collection_ranking(
            ranking_network, period=period, sortby=sortby
        )
        ranking = ranking["collections"]
        df_ranking = pd.DataFrame(ranking)

        ranking_columns = [
            "image",
            "id",
            "name",
            "volume",
            "volumePercentChange",
            "count",
            "countPercentChange",
        ]
        df_ranking = df_ranking[ranking_columns]

        st.dataframe(
            df_ranking,
            height=1000,
            use_container_width=True,
            hide_index=True,
            column_config={"image": st.column_config.ImageColumn("icon")},
        )

    def st_curation(self, network, collection_id):
        start_time = time.time()

        try:
            with st.status(
                f"⏳ Generating NFT Curation ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
                expanded=True,
            ):
                result_data = self.llm_instance(
                    network=network,
                    collection_id=collection_id,
                    image_counts=self.nft_image_counts,
                    max_tokens=self.max_tokens,
                )

                st.markdown(f"##### {result_data['generated']['title']}")

                st.write("###### short description")
                st.write(result_data["generated"]["description"])

                st.write("###### long description")
                st.write(result_data["generated"]["long_description"])

                st.markdown("###### tags")
                st.text(result_data["generated"]["tag"])

                elapsed_time = time.time() - start_time
                st.write(f"⏱️ Elapsed Time: {elapsed_time:.2f} sec")

                self.logger.info(
                    f"Network: {network}, Collection ID: {collection_id}, Elapsed Time: {elapsed_time:.2f} sec"
                )

                if result_data["source"]["collection"]["images"]:
                    image_select(
                        label="Source NFT Images",
                        images=result_data["source"]["collection"]["images"],
                        use_container_width=True,
                    )
                else:
                    st.error("No NFT Images")

            st.toast("Curation has been generated!", icon="✅")
        except openai.BadRequestError as E:
            st.write(E)

    def run(self):
        st.set_page_config(
            page_title="NFT Curation Bot",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        network, collection_id, is_click = self.st_sidebar()

        col_ranking, col_curations = st.columns(2)

        with col_ranking.container(border=True):
            self.st_ranking()

        with col_curations.container(border=True):
            st.header("Bot Curation")
            if is_click:
                for _ in range(self.question_count):
                    self.st_curation(network, collection_id)
