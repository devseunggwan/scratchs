import os
import random
import time
import logging

import httpx
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from streamlit_image_select import image_select


class NFTCurationBot:
    def __init__(self):
        self.openai = OpenAI()
        self.model = "gpt-4-turbo"

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
        self.reservoir_collection_url = (
            lambda x: f"https://{self.reservoir_networks_url_prefix[x]}.reservoir.tools/collections/v7"
        )
        self.reservoir_nft_list_url = (
            lambda x: f"https://{self.reservoir_networks_url_prefix[x]}.reservoir.tools/tokens/v7"
        )

        self.prompt = """
        역할
        - 당신은 NFT 컬렉션 전문가며 큐레이터를 하면서 사람들에게 NFT에 대해 내용을 전달하는 역할입니다.
        - 당신은 주어진 NFT 이미지를 기반으로 컬렉션에 대한 묘사 및 태그를 작성해야 합니다.

        지시사항
        1. 작성 항목 및 설명
            1-1. <컬랙션 이미지 묘사>
                - 진부하지 않고 생동감있게 표현해주세요.
                - 이미지의 주요 특징을 강조해주세요.
                - 이미지의 개별적인 묘사보다 종합적인 묘사를 작성해주세요.
            1-2. <컬랙션 태그>
                - 이미지를 종합적으로 확인하고 컬랙션을 대표하는 키워드를 작성해주세요.
                - NFT의 이름, NFT 이더리움, 블록체인 네트워크 같은 NFT에서 일반적으로 이야기하는 키워드를 넣지도 말고 포함하지도 말아주세요.
                - 개성, 다양성, 독창성, 창의성 같이 모호하고, 일반적, 진부적으로 이미지를 표현하는 키워드는 넣지 말아주세요.
                - 이미지 하나에서만 확인할 수 있는 키워드는 제외하고 작성해주세요.
                - NFT 컬랙션 이미지에 대해서 개별적인 묘사보다는 종합적인 묘사로 어올리는 키워드를 작성해주세요.
        2. 문장 작성 방법
            2-1. <컬랙션 이미지 묘사>
                - 평가와 묘사는 최대 500자로 제한합니다.
                - 만약 500자에서 문장이 마무리되지 않는다면, 300자 이상 작성해도 좋으니 문장을 마무리해주세요.
                - 평가와 묘사 등을 문단이나 구분해서 작성하지 말아주세요.
                - 컬랙션 이름을 작성할 떄는 원문 그대로 작성해주세요.
            2-2. <컬랙션 태그>
                - 컬랙션 태그는 평가 500자와 별개로 작성해주세요.
                - 태그는 List(str) 형태로 쉼표(,)로 구분해주시고 예시를 보고 꼭 지켜주세요. (예: ["태그1", "태그2", "태그3"])
                - 태그는 최소 10개 이상 작성해주세요.
                - 태그에 스페이스를 넣지 마세요.

        컬렉션 추가 정보
        - 컬렉션 이름: {collection_name}
        - 컬렉션 설명: {collection_description}

        출력 결과
        1. 출력 유의 사항
            - 답변은 한국어로 작성해주세요.
            - 문법, 맞춤법, 띄어쓰기를 꼭 지켜주세요.
            - 각각 항목들의 제목은 작성 안하셔도 됩니다.
            - 구분선(---)은 무조건 추가해주세요.
            - 꺽쇠(<>)로 둘러싸인 부분 안에 각각 내용을 작성합니다.
            - 꺽쇠(<>)로 둘러싸인 부분은 제거하고 작성해주세요.
        2. 출력 결과 예시
        <컬랙션 이미지 묘사>

        ---

        <컬랙션 태그>
        """

        self.logger = logging.getLogger(st.__name__)

    def st_sidebar(self):
        with st.sidebar:
            st.header("NFT Curation Bot")

            network = st.selectbox(
                "Network", list(self.reservoir_networks_url_prefix.keys())
            )
            collection_id = st.text_input("Collection ID")
            self.nft_image_counts = st.slider("NFT Images", 1, 20, 10, 1)
            self.max_tokens = st.slider("Max Tokens", 50, 1000, 500, 50)
            self.question_count = st.slider("Question Count", 1, 3, 1, 1)

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

    def get_nft_curation(self, nft_images, collection_name, collection_description):
        prompt = self.prompt.format(
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
            model="gpt-4-turbo",
            messages=messages,
            max_tokens=self.max_tokens,
        )

        return response.choices[0].message.content

    def run(self):
        network, collection_id, is_click = self.st_sidebar()

        st.header("Bot Curation")
        if is_click:
            self.logger.info(f"Network: {network}, Collection ID: {collection_id}")

            nft_images, collection_name, collection_description = self.get_nft_data(
                network, collection_id
            )

            if len(nft_images) == 0:
                st.warning("No NFT images available.")
                return

            for i in range(self.question_count):
                start_time = time.time()
                with st.status(f"⏳ Generating NFT Curation ({i + 1})", expanded=True):
                    nft_curations = self.get_nft_curation(
                        nft_images, collection_name, collection_description
                    )

                    st.write(nft_curations)

                    elapsed_time = time.time() - start_time
                    st.write(f"⏱️ Elapsed Time: {elapsed_time:.2f} sec")

                    self.logger.info(
                        f"Network: {network}, Collection ID: {collection_id}, Curation: {nft_curations}, Elapsed Time: {elapsed_time:.2f} sec"
                    )

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
