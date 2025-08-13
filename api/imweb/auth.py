import httpx

api_key = ""
secret_key = ""

resp = httpx.post(
    url="https://api.imweb.me/v2/auth",
    headers={
        "Content-Type": "application/json",
        "ACCESS-AFFILIATE": "laplacetec",
    },
    json={
        "key": api_key,
        "secret": secret_key,
    },
)
