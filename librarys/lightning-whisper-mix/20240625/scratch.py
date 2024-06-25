import json
import os

from lightning_whisper_mlx import LightningWhisperMLX
from tqdm import tqdm


def write_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False)


# https://github.com/mustafaaljadery/lightning-whisper-mlx
if __name__ == "__main__":
    # ["tiny", "small", "distil-small.en", "base", "medium", distil-medium.en", "large", "large-v2", "distil-large-v2", "large-v3", "distil-large-v3"]
    MODEL = "large-v3"
    BATCH_SIZE = 12
    # [None, "4bit", "8bit"]
    QUANTIZATION = None

    PATH_VOICE = "./data/voices"
    PATH_OUTPUT = "./data/output/{voice_file}.json"

    list_voice = tqdm(os.listdir(PATH_VOICE))

    whisper = LightningWhisperMLX(
        model=MODEL, batch_size=BATCH_SIZE, quant=QUANTIZATION
    )

    for voice_file in list_voice:
        list_voice.set_description(voice_file)

        path_voice_file = os.path.join(PATH_VOICE, voice_file)
        translate = whisper.transcribe(audio_path=path_voice_file)

        resp = {"file_name": voice_file, "original": translate}

        write_json(resp, PATH_OUTPUT.format(voice_file=voice_file))
