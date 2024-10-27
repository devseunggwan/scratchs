import sys


def read():
    input = sys.stdin.readline
    TC = int(input())

    CASES = []

    for _ in range(TC):
        case = {
            "word": [input().strip() for _ in range(int(input()))],
            "info": [
                list(map(int, input().strip().split()))[1:] for _ in range(int(input()))
            ],
        }

        CASES.append(case)

    return CASES


def get_password(word, info):
    return "".join([word[x] for x in info])


if __name__ == "__main__":
    for idx, case in enumerate(read()):
        print(f"Scenario #{idx + 1}:")
        word, infos = case["word"], case["info"]

        for info in infos:
            print(get_password(word, info))

        print("")
