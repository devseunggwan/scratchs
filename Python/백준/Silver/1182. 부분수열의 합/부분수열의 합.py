import sys
from itertools import combinations


def read():
    input = sys.stdin.readline

    N, S = map(int, input().strip().split())
    M = list(map(int, input().strip().split()))

    return N, S, M


if __name__ == "__main__":
    N, S, M = read()
    answer = 0

    for i in range(1, N + 1):
        for j in combinations(M, i):
            if sum(j) == S:
                answer += 1

    print(answer)
