import os
import random
from datetime import datetime, timedelta

from dotenv import load_dotenv
from locust import HttpUser, TaskSet, between, task

load_dotenv(verbose=True, override=True)


class CollectionService(TaskSet):
    def on_start(self) -> None:
        self._headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("X_API_KEY"),
        }
        self.collections = [
            "0x5af0d9827e0c53e4799bb226655a1de152a425a5",
            "0xbd3531da5cf5857e7cfaa92426877b022e612cf8",
            "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",
            "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb",
            "0x769272677fab02575e84945f03eca517acc544cc",
            "0x60e4d786628fea6478f785a6d7e704777c86a7c6",
            "0x524cab2ec69124574082676e6f654a18df49a048",
            "0xe42cad6fc883877a76a26a16ed92444ab177e306",
            "0x39ee2c7b3cb80254225884ca001f57118c8f21b6",
            "0xb63ce3ac885a3318fc2e563fdb190e9a5dda5b33",
            "0xbe9371326f91345777b04394448c23e2bfeaa826",
        ]

    @staticmethod
    def generate_random_date(start_date: datetime, end_date: datetime):
        random_date = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        return random_date.strftime("%Y-%m-%d")

    def request(self, url):
        __collection = random.choice(self.collections)
        __params = {
            "collectionId": __collection,
            "startDate": self.generate_random_date(
                datetime(2023, 12, 20), datetime(2023, 12, 30)
            ),
            "endDate": self.generate_random_date(
                datetime(2024, 6, 20), datetime(2024, 6, 30)
            ),
        }

        self.client.get(url, params=__params, headers=self._headers)

    @task
    def collection_floorprice(self):
        __url = "/svc/v1/collection/floor-price"
        self.request(__url)

    @task
    def collection_volume(self):
        __url = "/svc/v1/collection/volume"
        self.request(__url)


class LocustUser(HttpUser):
    host = os.getenv("HOST")
    tasks = [CollectionService]
    wait_time = between(1, 4)
