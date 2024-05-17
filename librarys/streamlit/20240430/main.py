import logging
import os
import random
import time

import httpx
import openai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from streamlit_image_select import image_select


class NFTCurationBot:
    def __init__(self):
        self.openai = OpenAI()
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

        self.prompt_description = """
1. 역할
- 당신은 NFT 컬렉션 전문가며 큐레이터를 하면서 사람들에게 NFT에 대해 내용을 전달하는 역할입니다.
- 당신은 주어진 NFT 이미지를 기반으로 컬렉션에 대한 묘사를 작성해야 합니다.

2. 작성 항목 및 설명
- 진부하지 않고 생동감있게 표현해주세요.
- 이미지의 주요 특징을 강조해주세요. 
- 첫번째, 두번째 이미지는 어떻다. 라고 설명하지말고 말아주세요.
- 이미지의 개별적인 묘사보다 종합적인 묘사를 작성해주세요.
    
3. 문장 작성 방법
- 답변은 한국어로 작성해주세요.
- 평가와 묘사는 최대 200자로 제한합니다.
- 평가와 묘사 등을 문단이나 구분해서 작성하지 말아주세요.
- 컬랙션 이름을 작성할 떄는 원문 그대로 작성해주세요.
- 문법, 맞춤법, 띄어쓰기를 꼭 지켜주세요.

4. 추가 정보
- 컬렉션 이름: {collection_name}
- 컬렉션 설명: {collection_description}
"""
        self.prompt_tag = """
1. 역할
- 당신은 NFT 컬렉션 전문가며 큐레이터를 하면서 사람들에게 NFT에 대해 내용을 전달하는 역할입니다.
- 당신은 주어진 NFT 이미지, 이름, 설명과 이를 바탕으로 요약된 내용을 기반으로 컬렉션에 대한 태그를 작성해야 합니다.

2. 작성 항목 및 설명
- 이미지를 종합적으로 확인하고 컬랙션을 대표하는 키워드를 작성해주세요.
- NFT의 이름, NFT 이더리움, 블록체인 네트워크 같은 NFT에서 일반적으로 이야기하는 키워드를 넣지도 말고 포함하지도 말아주세요.
- 개성, 다양성, 독창성, 창의성 같이 모호하고, 일반적, 진부적으로 이미지를 표현하는 키워드는 넣지 말아주세요.
- 이미지 하나에서만 확인할 수 있는 키워드는 제외하고 작성해주세요.
- NFT 컬랙션 이미지에 대해서 개별적인 묘사보다는 종합적인 묘사로 어올리는 키워드를 작성해주세요.

3. 문장 작성 방법
- 태그는 List(str) 형태로 쉼표(,)로 구분해주시고 예시를 보고 꼭 지켜주세요. (예: ["태그1", "태그2", "태그3"])
- 태그는 8~10개 작성해주세요.
- 태그에 스페이스를 넣지 마세요.
- 태그는 한국어로만 작성해주세요.

4. 추가 정보
- 컬렉션 이름: {collection_name}
- 컬렉션 설명: {collection_description}
- 컬랙션 요약: {ai_curation}
"""
        self.prompt_curation = """
1. 역할
- 당신은 NFT 컬렉션 전문가며 큐레이터를 하면서 사람들에게 NFT에 대해 내용을 전달하는 역할입니다.
- 당신은 NFT 컬랙션에 대한 요약과 태그를 보고 종합적으로 한 줄 요약이 필요합니다.
- 45자 이상 55자 사이의 한국어 문장으로 작성해주세요.
- 마지막에 NFT 컬랙션 이라는 워딩을 사용하지 마세요.

2. 출력 결과 예시
- 일본의 역사적 상징인 사무라이를 NFT 애니메이션으로 만나다
- 스트릿 스타일 네오치비 PFP NFT, 밝고 생기 있는 컬러 팔레트가 특징
- 2017년 시작된 픽셀 아트, 독창적 캐릭터로 디지털 예술을 혁신
- 도시의 개성 넘치는 'Personas'와 Timefall Valley의 다채로운 스토리
- 미래지향적 큐브 NFT, 첨단 기술과 빛의 교차가 돋보임
- 20세기 마스터들의 영감을 현대적 콜라주로 재해석

3. NFT 컬랙션에 대한 요약
{ai_curation}
"""

        self.logger = logging.getLogger(st.__name__)

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
                self.prompt_description = st.text_area(
                    "Prompt Description",
                    self.prompt_description,
                    height=500,
                    label_visibility="collapsed",
                )
            with st.expander("Prompt - NFT 태그"):
                self.prompt_tag = st.text_area(
                    "Prompt Tag",
                    self.prompt_tag,
                    height=500,
                    label_visibility="collapsed",
                )
            with st.expander("Prompt - NFT 한줄 요약"):
                self.prompt_curation = st.text_area(
                    "Prompt Curation",
                    self.prompt_curation,
                    height=500,
                    label_visibility="collapsed",
                )

            is_click = st.button("Run")

            return network, collection_id, is_click

    def get_nft_data(self, network, collection_id):
        params = {
            "id": collection_id,
        }
        collection = httpx.get(
            self.reservoir_collection_url(network), params=params, headers=self.headers
        ).json()

        params = {"collection": collection_id, "sortBy": "updatedAt", "limit": 100}
        nft_list = httpx.get(
            self.reservoir_nft_list_url(network), params=params, headers=self.headers
        ).json()

        collection_name = (
            collection["collections"][0]["name"]
            if len(collection["collections"]) > 0
            else ""
        )
        collection_description = (
            collection["collections"][0]["description"]
            if len(collection["collections"]) > 0
            else ""
        )
        nft_images = (
            random.choices(
                [
                    nft["token"]["imageSmall"]
                    for nft in nft_list["tokens"]
                    if "imageSmall" in nft["token"]
                    and nft["token"]["imageSmall"] is not None
                    and "bmp" not in nft["token"]["imageSmall"]
                ],
                k=self.nft_image_counts,
            )
            if len(nft_list["tokens"]) > 0
            else []
        )

        return nft_images, collection_name, collection_description

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

    def get_nft_description(self, nft_images, collection_name, collection_description):
        prompt = self.prompt_description.format(
            collection_name=collection_name,
            collection_description=collection_description,
        )

        nft_images = [
            {"type": "image_url", "image_url": {"url": image}} for image in nft_images
        ]

        content = [{"type": "text", "text": prompt}]
        content.extend(nft_images)

        messages = [{"role": "user", "content": content}]

        response = self.openai.chat.completions.create(
            model=self.model, messages=messages, max_tokens=self.max_tokens
        )

        return response.choices[0].message.content

    def get_nft_tag(
        self, nft_images, collection_name, collection_description, ai_curation
    ):
        prompt = self.prompt_tag.format(
            collection_name=collection_name,
            collection_description=collection_description,
            ai_curation=ai_curation,
        )

        nft_images = [
            {"type": "image_url", "image_url": {"url": image}} for image in nft_images
        ]

        content = [{"type": "text", "text": prompt}]
        content.extend(nft_images)

        messages = [{"role": "user", "content": content}]

        response = self.openai.chat.completions.create(
            model=self.model, messages=messages, max_tokens=self.max_tokens
        )

        return response.choices[0].message.content

    def get_nft_curation(self, ai_curation):
        prompt = self.prompt_curation.format(
            ai_curation=ai_curation,
        )
        content = [{"type": "text", "text": prompt}]
        messages = [{"role": "user", "content": content}]

        response = self.openai.chat.completions.create(
            model=self.model, messages=messages, max_tokens=self.max_tokens
        )
        return response.choices[0].message.content

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

        with col_curations.container(border=True):
            st.header("Bot Curation")
            if is_click:
                nft_images, collection_name, collection_description = self.get_nft_data(
                    network, collection_id
                )

                if len(nft_images) == 0:
                    st.warning("No NFT images available.")
                    return

                for i in range(self.question_count):
                    start_time = time.time()

                    try:
                        with st.status(
                            f"⏳ Generating NFT Curation ({i + 1})", expanded=True
                        ):
                            nft_description = self.get_nft_description(
                                nft_images, collection_name, collection_description
                            )
                            nft_tag = self.get_nft_tag(
                                nft_images,
                                collection_name,
                                collection_description,
                                nft_description,
                            )
                            nft_curation = self.get_nft_curation(nft_description)

                            st.markdown("##### 큐레이션 한마디")
                            st.write(nft_curation)
                            st.markdown("##### NFT 설명")
                            st.write(nft_description)
                            st.markdown("##### NFT 태그")
                            st.write(nft_tag)

                            elapsed_time = time.time() - start_time
                            st.write(f"⏱️ Elapsed Time: {elapsed_time:.2f} sec")

                            self.logger.info(
                                f"Network: {network}, Collection ID: {collection_id}, Elapsed Time: {elapsed_time:.2f} sec"
                            )
                    except openai.BadRequestError as E:
                        st.write(E)

                st.subheader("NFT Description")
                st.write(collection_description)
                image_select(
                    label="Source NFT Images",
                    images=nft_images,
                    use_container_width=True,
                )
                st.toast("Curation has been generated!", icon="✅")


if __name__ == "__main__":
    load_dotenv()
    bot = NFTCurationBot()
    bot.run()
