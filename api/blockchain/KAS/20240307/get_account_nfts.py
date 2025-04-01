import json
import os
import asyncio

import aiohttp
from dotenv import load_dotenv


async def fetch(session, url):
    async with session.get(url) as response:
        if response.headers["Content-Type"] == "application/octet-stream":
            data = await response.read()
            data = data.decode("utf-8")

            data = json.loads(data)

            return data

        return await response.json()


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(
            *[fetch(session, url) for url in urls], return_exceptions=True
        )
        return results


async def main():
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            __url,
            headers=__headers,
        )
        resp = await resp.json()

        token_uris = [
            item["extras"]["tokenUri"]
            for item in resp["nfts"]
            if "extras" in item and "tokenUri" in item["extras"]
        ]

        results = await fetch_all(token_uris, asyncio.get_event_loop())

        for item, result in zip(resp["items"], results):
            if "extras" in item and "tokenUri" in item["extras"]:
                item["extras"]["tokenUri"] = result

    return resp


if __name__ == "__main__":
    load_dotenv()

    import time

    start = time.time()

    __headers = {
        "x-api-key": os.getenv("OPENSEA_API_KEY"),
        "Content-Type": "application/json",
    }

    __chain = "klaytn"
    __address = os.getenv("SAMPLE_ADDR")
    __url = f"https://api.opensea.io/api/v2/chain/{__chain}/account/{__address}/nfts"

    loop = asyncio.get_event_loop()
    resp = loop.run_until_complete(main())

    end = time.time() - start

    print(f"Time: {end:.2f} seconds")

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(resp, f, indent=4, ensure_ascii=False)
