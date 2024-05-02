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
        self.reservoir_collection_url = "https://api.reservoir.tools/collections/v7"
        self.reservoir_nft_list_url = "https://api.reservoir.tools/tokens/v7"

        self.prompt = """
            You are an NFT expert.
            1. Please look at the NFT images provided and a comprehensive evaluation.
            2. Please express the appearance of picture vividly.
            3. Please write up to 300 characters in length.
            4. Please write it in Korean.
            
            Collection Name: {collection_name}
            Collection Description: {collection_description}
        """

        self.logger = logging.getLogger(st.__name__)

    def st_sidebar(self):
        with st.sidebar:
            st.header("NFT Curation Bot")

            network = st.text_input("Network", value="ethereum")
            collection_id = st.text_input("Collection ID")
            self.nft_image_counts = st.slider("NFT Images", 1, 20, 10, 1)
            self.max_tokens = st.slider("Max Tokens", 50, 500, 300, 50)
            self.question_count = st.slider("Question Count", 1, 3, 1, 1)

            is_click = st.button("Run")

            st.warning(
                "현재 이더리움만 지원하고 있습니다. 이더리움 컬랙션만 테스트 부탁드립니다.",
                icon="🚨",
            )

            return network, collection_id, is_click

    def get_nft_data(self, collection_id):
        params = {
            "id": collection_id,
        }
        collection = httpx.get(
            self.reservoir_collection_url, params=params, headers=self.headers
        ).json()

        params = {"collection": collection_id, "sortBy": "updatedAt", "limit": 100}
        nft_list = httpx.get(
            self.reservoir_nft_list_url, params=params, headers=self.headers
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
                collection_id
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
