import sys


def read():
    input = sys.stdin.readline

    N, K = map(int, input().strip().split())
    BAG = [list(map(int, input().strip().split())) for _ in range(N)]

    return N, K, BAG


if __name__ == "__main__":
    N, K, BAG = read()
    DP = [[0 for _ in range(K + 1)] for _ in range(N + 1)]

    for i in range(1, N + 1):
        w, v = BAG[i - 1]

        for j in range(1, K + 1):
            if j - w < 0:
                DP[i][j] = DP[i - 1][j]
                continue

            DP[i][j] = max(DP[i - 1][j], DP[i - 1][j - w] + v)

    print(DP[-1][-1])
