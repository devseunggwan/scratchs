import json
import os
import random
import re
from datetime import datetime

import httpx
from openai import OpenAI


class NftCurationLLM:
    def __init__(self):
        self.openai = OpenAI()
        self.model = "gpt-4o"
        self.image_counts = 15
        self.max_tokens = 500

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

        self.prompt_description = """
1. 역할
- 당신은 NFT 컬렉션 전문가며 큐레이터를 하면서 사람들에게 NFT에 대해 내용을 전달하는 역할입니다.
- 당신은 주어진 NFT 이미지를 기반으로 컬렉션에 대한 묘사를 작성해야 합니다.

2. 작성 항목 및 설명
- 답변은 한국어로 작성해주세요.
- 진부하지 않고 생동감있게 표현해주세요.
- 이미지의 주요 특징을 강조해주세요. 
- 이미지의 개별적인 묘사보다 종합적인 묘사를 작성해주세요.
- 반말로 작성하지 마세요.
- 명사형 종결문, 해라체, 서술형 등 종결 어미로 절대 작성하지 마세요.
- 컬랙션 이름:, 컬랙션 설명:, 컬랙션 이름 - 등 워딩을 사용하지 마세요.
- 첫번째, 두번째 이미지는 어떻다. 같이 각각 이미지를 설명하지 말아주세요.
- 평가와 묘사는 최대 {max_korean_token_length}자로 제한합니다.
- 컬랙션 이름을 작성할 떄는 원문 그대로 작성해주세요.
- 문법, 맞춤법, 띄어쓰기를 꼭 지켜주세요.

3. 추가 정보
- 컬렉션 이름: {collection_name}
- 컬렉션 설명: {collection_description}

4. 결과 예시
- Shit Grins 컬렉션은 단순하면서도 강렬한 웃음을 담고 있습니다. 섬세한 선으로 그려진 이 이미지는 각기 다른 표정을 통해 유쾌하고 익살스러운 분위기를 자아내며, 모든 표정들이 하찮게 여겨질 수도 있는 순간들에 대한 유머와 기쁨을 전합니다. 눈이 X자로 되어 있거나 풍자적인 웃음을 띈 얼굴들이 이 컬렉션의 매력을 높입니다. 이 머리완성되지 않은 스케치들은 보는 이로 하여금 각자의 해석을 더해 완성해 나가도록 합니다.
- Friendly Beasts 컬렉션은 현대 디지털 아트의 따뜻한 매력을 총족실히 보여줍니다. 각 작품은 동물들과 여타 자연 요소들을 독특하고 친근한 방식으로 재해석하여, 사람들에게 자연과의 연결을 더욱 깊게 생각하게 만듭니다. 따뜻한 색감과 선명한 디테일은 보는 이로 하여금 자연 속에 있는 듯한 생생한 느낌을 받게 합니다. 귀여운 동물의 일상 속 순간들을 포착한 이 이미지는 단순한 그림을 넘어서, 각자 개별적인 이야기를 상상하게 만듭니다. Friendly Beasts는 동물과 자연을 사랑하는 모든 이들에게 완벽한 예술적 경험을 제공합니다.
- Azuki 컬렉션은 매력적이면서도 독특한 스타일의 아바타들이 빚어내는 환상의 공간입니다. 각 아바타는 개성 넘치는 모습과 디테일한 요소들로 구성되어, 전통과 현대가 어우러지는 분위기를 표현합니다. 강렬한 색감과 굵은 선을 사용하여 캐릭터들의 감정과 태도가 생생하게 전달됩니다. 일본 전통 복장을 재해석한 의상부터 독특한 소품까지, 각 아바타는 독자적인 이야기를 담고 있으며, 이를 통해 'The Garden'이라는 인터넷 구석에서 만나 서로 교류하고 성장할 수 있는 회원이 됩니다. Azuki 컬렉션은 예술가, 창작자, 그리고 웹3 애호가들이 모여 탈중앙화된 미래를 꿈꾸는데 완벽한 플랫폼을 제공합니다.
- Lil Pudgys는 22,222개의 NFT로 구성된 컬렉션으로, Pudgy Penguins의 연장선에서 등장했습니다. 이 작은 펭귄들은 크기는 작지만 큰 의미와 역사를 담고 있습니다. 특히 겨울의 혹독한 시기 동안 태어난 이들은 공동체에 새로운 생명을 불어넣었습니다. 이 컬렉션은 각 Lil Pudgy가 독특한 특징과 성격을 지녀, 진정한 다양성과 유쾌함을 보여줍니다. 귀여운 외모와 함께 다양한 액세서리와 의상, 그리고 생동감 넘치는 표정들이 포함되어 있으며, 이는 다양한 문화와 개성을 반영합니다. Lil Pudgy 소유자들은 특별한 경험과 이벤트, 지적 재산권 라이선싱 기회 등을 독점적으로 누릴 수 있습니다. 이러한 요소들이 더해져 Lil Pudgys는 단순한 수집품을 넘어 더욱 풍부하고 연결된 커뮤니티를 만들고 있습니다.
- Galaxy Habbos 컬렉션은 미래의 디지털 유토피아를 그린 픽셀아트 스타일의 세계를 담아냅니다. 각 이미지에서 나타나는 화려한 네온 빛깔과 정교한 픽셀 배치는 디지털의 발전과 그 무한한 가능성을 상징합니다. 사람 형상의 실루엣은 각 이미지마다 공통되게 등장하나, 주변의 디지털 렌더링과 함께 유니크함을 주는 요소들을 갖추고 있어 독특한 아우라를 자아냅니다. 어두운 배경이 인물의 형상을 더 돋보이게 만들며, 미래 지향적이고 SF적인 분위기를 연출하여 한눈에 끌리게 합니다. Galaxy Habbos는 디지털 예술의 새로운 경계를 보여주며, 가상 세계 속에서만 가능한 환상적인 분위기를 완벽히 담고 있습니다.
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

    @staticmethod
    def filter_image_url(image_urls: list[str]) -> list[str]:
        return [
            image_url
            for image_url in image_urls
            if re.match(
                r".*(png|jpeg|gif|webp).*",
                image_url,
                re.IGNORECASE,
            )
        ]

    def get_collection_data(self, network, collection_id):
        params = {
            "id": collection_id,
        }
        collection = httpx.get(
            self.reservoir_collection_url(network), params=params, headers=self.headers
        ).json()

        params = {"collection": collection_id, "sortBy": "updatedAt", "limit": 1000}
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
        nft_images = [
            nft["token"]["imageSmall"]
            for nft in nft_list["tokens"]
            if "imageSmall" in nft["token"] and nft["token"]["imageSmall"] is not None
        ]
        nft_images = self.filter_image_url(nft_images)

        nft_images = (
            random.choices(
                nft_images,
                k=self.image_counts,
            )
            if nft_images
            else []
        )

        return nft_images, collection_name, collection_description

    def get_collection_description(
        self,
        nft_images,
        collection_name,
        collection_description,
        max_korean_token_length=200,
    ):
        prompt = self.prompt_description.format(
            max_korean_token_length=max_korean_token_length,
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
            model=self.model, messages=messages, max_tokens=self.max_tokens, timeout=60
        )

        result = response.choices[0].message.content
        result = result.strip()

        return result

    def get_collection_tag(
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
            model=self.model, messages=messages, max_tokens=self.max_tokens, timeout=60
        )

        result = response.choices[0].message.content
        result = json.loads(result)

        return result

    def get_collection_description_title(self, ai_curation):
        prompt = self.prompt_curation.format(
            ai_curation=ai_curation,
        )
        content = [{"type": "text", "text": prompt}]
        messages = [{"role": "user", "content": content}]

        response = self.openai.chat.completions.create(
            model=self.model, messages=messages, max_tokens=self.max_tokens, timeout=60
        )

        result = response.choices[0].message.content
        result = result.strip()

        return result

    def __call__(self, network, collection_id, image_counts=15, max_tokens=500):
        self.image_counts = image_counts
        self.max_tokens = max_tokens

        nft_images, collection_name, collection_description = self.get_collection_data(
            network=network, collection_id=collection_id
        )

        nft_description = self.get_collection_description(
            nft_images, collection_name, collection_description
        )
        nft_long_description = self.get_collection_description(
            nft_images, collection_name, collection_description, 1000
        )

        nft_tag = self.get_collection_tag(
            nft_images,
            collection_name,
            collection_description,
            nft_description,
        )
        nft_desc_title = self.get_collection_description_title(nft_description)

        result_data = {
            "source": {
                "network": network,
                "collection": {
                    "id": collection_id,
                    "name": collection_name,
                    "description": collection_description,
                    "images": nft_images,
                },
            },
            "generated": {
                "title": nft_desc_title,
                "description": nft_description,
                "long_description": nft_long_description,
                "tag": nft_tag,
            },
            "metadata": {
                "model": self.model,
                "image_counts": self.image_counts,
                "max_tokens": self.max_tokens,
            },
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return result_data
