from time import time

import bcrypt
import httpx
import pybase64

client_id = ""
client_secret = ""
account_id = ""

timestamp_for_cert = int(round(time() * 1000))
password = client_id + "_" + str(timestamp_for_cert)
hashed = bcrypt.hashpw(password.encode("utf-8"), client_secret.encode("utf-8"))
cert_str = pybase64.standard_b64encode(hashed).decode("utf-8")
params = {
    "client_id": client_id,
    "timestamp": timestamp_for_cert,
    "client_secret_sign": cert_str,
    "grant_type": "client_credentials",
    "type": "SELLER",
    "account_id": account_id,
}

resp = httpx.post(
    url="https://api.commerce.naver.com/partner/v1/oauth2/token",
    params=params,
    headers={"content-type": "application/x-www-form-urlencoded"},
)

print(resp.json())
