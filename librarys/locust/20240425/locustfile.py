import os
import random

import pandas as pd
from locust import HttpUser, task, between, TaskSet
from dotenv import load_dotenv

load_dotenv()


df = pd.read_csv("./assets/klaytn.csv")
dict_df = df.to_dict(orient="records")


class Collections(TaskSet):
    def on_start(self) -> None:
        self._headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("X_API_KEY"),
        }

    @task
    def get_collection_info(self):
        __url = "/svc/v1/collection/info"

        __nft = random.choice(dict_df)
        __params = {
            "network": __nft["NETWORK"],
            "collectionId": __nft["COLLECTION_ID"],
        }
        self.client.get(__url, params=__params, headers=self._headers)

    @task
    def get_collection_transaction(self):
        __url = "/svc/v1/collection/transaction"

        __nft = random.choice(dict_df)
        __params = {
            "network": __nft["NETWORK"],
            "collectionId": __nft["COLLECTION_ID"],
        }
        self.client.get(__url, params=__params, headers=self._headers)


class Nfts(TaskSet):
    def on_start(self) -> None:
        self._headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("X_API_KEY"),
        }

    @task
    def get_nft_info(self):
        __url = "/svc/v1/nft/info"
        __nft = random.choice(dict_df)
        __params = {
            "network": __nft["NETWORK"],
            "collectionId": __nft["COLLECTION_ID"],
            "tokenId": random.randint(1, 10000),
        }
        self.client.get(__url, params=__params, headers=self._headers)

    @task
    def get_nft_list(self):
        __url = "/svc/v1/nft/list"
        __nft = random.choice(dict_df)
        __params = {
            "network": __nft["NETWORK"],
            "collectionId": __nft["COLLECTION_ID"],
        }
        self.client.get(__url, params=__params, headers=self._headers)

    @task
    def get_nft_transaction(self):
        __url = "/svc/v1/nft/transaction"
        __nft = random.choice(dict_df)
        __params = {
            "network": __nft["NETWORK"],
            "collectionId": __nft["COLLECTION_ID"],
            "tokenId": random.randint(1, 10000),
        }
        self.client.get(__url, params=__params, headers=self._headers)

    @task
    def get_nft_aggregation(self):
        __url = "/svc/v1/nft/aggregation"
        __nft = random.choice(dict_df)
        __params = {
            "network": __nft["NETWORK"],
            "collectionId": __nft["COLLECTION_ID"],
            "tokenId": random.randint(1, 10000),
        }
        self.client.get(__url, params=__params, headers=self._headers)


class LocustUser(HttpUser):
    host = os.getenv("HOST")
    tasks = [Collections, Nfts]
    wait_time = between(1, 4)
