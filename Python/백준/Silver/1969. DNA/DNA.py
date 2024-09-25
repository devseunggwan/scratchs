from collections import Counter


def read():
    N, M = map(int, input().strip().split())

    DNA = [input() for _ in range(N)]

    return N, M, DNA


if __name__ == "__main__":
    N, M, DNA = read()

    DNA = [
        sorted(
            Counter([DNA[j][i] for j in range(N)]).items(),
            key=lambda x: (-x[1], x[0]),
        )[0]
        for i in range(M)
    ]
    print("".join([x[0] for x in DNA]))
    print(sum([N - x[1] for x in DNA]))
