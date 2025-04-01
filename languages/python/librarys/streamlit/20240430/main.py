from dotenv import load_dotenv
from service import NftCurationLLM
from view import NftCurationUI

if __name__ == "__main__":
    load_dotenv()

    llm = NftCurationLLM()
    ui = NftCurationUI(llm)
    ui.run()
