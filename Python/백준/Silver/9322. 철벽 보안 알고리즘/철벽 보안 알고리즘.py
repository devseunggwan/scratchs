import sys


def read():
    input = sys.stdin.readline

    TC = int(input())
    cases = [
        [
            int(input()),
            input().strip().split(),
            input().strip().split(),
            input().strip().split(),
        ]
        for _ in range(TC)
    ]

    return cases


if __name__ == "__main__":
    cases = read()

    for case in cases:
        N, crypo_key1, crypo_key2, crypo_word = case
        key = [0] * N

        for i in range(N):
            for j in range(N):
                if crypo_key1[i] == crypo_key2[j]:
                    key[i] = j
                    break

        print(" ".join([crypo_word[x] for x in key]))
