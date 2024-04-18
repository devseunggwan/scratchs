import random
from locust import HttpUser, task, between, TaskSet

TOKENS = [
    "USD",
    "KRW",
    "ETH",
    "SOL",
    "KLAY",
    "MATIC",
    "FLOW",
    "AVAX",
    "OP",
    "BNB",
    "MANA",
    "BTC",
    "ARB",
    "WETH",
    "WKLAY",
    "SAND",
    "USDC",
    "PRIME",
    "WBNB",
    "GXA",
]


class UserBehavior(TaskSet):
    @task
    def get_user_detail(self):
        from_currency = random.choice(TOKENS)
        to_currency = random.choice(TOKENS)

        self.client.get(
            "/test", params={"from_currency": from_currency, "to_currency": to_currency}
        )


class LocustUser(HttpUser):
    host = "http://127.0.0.1:8000"
    tasks = [UserBehavior]
    wait_time = between(1, 4)
