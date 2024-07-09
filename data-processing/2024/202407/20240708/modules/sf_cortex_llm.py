import json
import time

from dotenv import load_dotenv
from snowflake.snowpark import Session

load_dotenv(dotenv_path=".env", verbose=True, override=True)


class SfCortexLLM:
    def __init__(self, session: Session, model_name: str, model_options: dict) -> None:
        self.session = session

        self.model_name = model_name
        self.model_options = model_options

        self.prompt_system = """
        - 콜센터에서 고객과의 음성대화를 텍스트로 변환한 데이터를 제공드립니다. 이에 대해서 출력형태에 맞게 작성해주세요. 
        - 답변은 한글로 작성해주시고, 맞춤법을 지켜주세요.
        - 사람 이름이나 기업 정보, 휴대폰 번호, 주소, 계좌 번호 등을 답변에 제공하면 안됩니다. (효성, FMS는 기업 정보입니다.)
        - Json 형식을 요청할 것이고 이후, Python json 라이브러리를 사용하여 파싱할겁니다. 라이브러리 에러가 나지 않게 답변 형식을 지켜주세요.
        """

        self.prompt_voice = """
        <음성대화>
        {voice}
        """

        self.prompt_summary = """
        <요청 사항>
        - 제목(title)은 음성 대화를 가장 잘 설명할 수 있는 제목으로 100자 이내로 작성해주세요.
        - 설명(description)은 음성 대화의 문맥을 파악 후, 경영진, 의사결정자에게 설명하듯이 상세하게 300자 내외로 설명해주세요.

        <출력 형태>
        {"title": "제목(title) 출력 위치", "description": "설명(description) 출력 위치"}
        """

        self.prompt_categories = """
        <요청 사항>
        - 고객이 상담사에게 문의하는 내용을 설명할 수 있는 단어를 최대 5가지 선택하고, 이를 카테고리(category)로 출력해주세요.
        - 만약 설명할 수 있는 카테고리가 없다면 출력하지 마세요.
        - 문의, 전화, 상담, 지원 등 대화 상황에 대한 내용이 아닌 문맥의 내용에 맞게 선정해주세요.

        <출력 형태>
        {"categories": ["카테고리 1", "카테고리 2", "카테고리 3", "카테고리 4", "카테고리 5"]}
        """

        self.prompt_tags = """
        <요청 사항>
        - 제시하는 태그 중에 해당 음성 대화에 가장 어올리는 것으로 최대 5가지 선택해주세요.
        - 목록에 해당되지 않는 태그는 제공되면 안됩니다. 또한 문맥에 맞지 않는 태그는 선택되어선 안됩니다.

        <태그 목록>
        출금, 세무, 확인, 오류, 결제, 신청, 포털, 변경, 지연, 등록, 계좌, 전산, 입금, 자동이체, 해지, 처리, 회원, 동의서, 문제, 안내, 재출금, 수수료, 출금일, 인출, 수정, 취소, 실패

        <출력 형태>
        {"tags": ["태그 1", "태그 2", "태그 3", "태그 4", "태그 5"]}
        """

        self.prompt_sentiments = """
        <요청 사항>
        - 고객이 느끼고 있는 감정(sentiments)을 5가지 선정해주시고 리스트 형태로 출력해주세요. 그리고 고객이 느끼고 있는 감정에 대한 설명도 함께 작성해주세요.
        - 설명 받음, 답변, 기다림, 질문, 추가 문의 필요, 안내 등 감정이라고 판단되지 않는 글자는 제공되어선 안됩니다.
        - 감정 예시를 함께 첨부해드리니 이를 참고해서 감정을 선정해주세요.

        <감정 예시>
        감사, 궁금함, 불안, 혼동, 이해, 긍정적, 당황, 기대, 긴장, 긍정, 확인, 만족, 불만, 고민, 경의, 불편함, 혼란, 놀람, 불편, 부정, 걱정, 경계, 부정적, 안도, 불확실함, 어려움, 실망, 우려, 의아함, 평온함, 서슴, 화남, 낙담

        <출력 형태>
        {"sentiments": ["감정 1", "감정 2", "감정 3", "감정 4", "감정 5"],"sentiments_description": "감정 설명 작성 위치"}
        """

    @staticmethod
    def parse_complete(data: tuple):
        data = json.loads(data[0]["RES"])
        data["choices"] = json.loads(data["choices"][0]["messages"])

        return data

    @staticmethod
    def sf_cortex_complete(
        session: Session, model_name: str, prompts: dict[str, str], model_options: dict
    ):
        prompt_system = prompts["system"]
        prompt_concept = prompts["concept"]
        prompt_voice = prompts["voice"]

        query = (
            """
            SELECT 
                SNOWFLAKE.CORTEX.COMPLETE(
                    ?,
                    [
                        {
                            'role': 'system',
                            'content': '''
                            """
            + prompt_system
            + """
                            '''
                        },
                        {
                            'role': 'user',
                            'content': '''
                            """
            + prompt_concept
            + prompt_voice
            + """
                            '''
                        }
                    ],
                    {
                        'temperature': ?,
                        'max_tokens': ?
                    }
                ) AS RES
        """
        )

        return session.sql(
            query,
            params=[
                model_name,
                model_options["temperature"],
                model_options["max_tokens"],
            ],
        ).collect()

    def get_complete(
        self,
        session: Session,
        model_name: str,
        prompts: dict[str, str],
        model_options: dict,
    ):
        __resp = self.sf_cortex_complete(session, model_name, prompts, model_options)
        __resp = self.parse_complete(__resp)

        return __resp

    def run(self, voice):
        __summary = {}
        start = time.time()

        for prompt in [
            self.prompt_summary,
            self.prompt_categories,
            self.prompt_tags,
            self.prompt_sentiments,
        ]:
            __prompts = {
                "system": self.prompt_system,
                "concept": prompt,
                "voice": self.prompt_voice.format(voice=voice),
            }

            __resp = self.get_complete(
                self.session, self.model_name, __prompts, self.model_options
            )
            __summary = __summary | __resp["choices"]

        __summary["llm"] = {
            "model_name": self.model_name,
            "model_options": self.model_options,
            "elapsed_time": round(time.time() - start, 2),
        }

        return __summary
