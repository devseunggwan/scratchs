import sys


def read():
    input = sys.stdin.readline

    N = int(input())
    M = sorted([input().strip().split() for _ in range(N)], key=lambda x: int(x[1]))

    return N, M


if __name__ == "__main__":
    answer = ""
    N, M = read()

    for S, _, D in M:
        answer += S[int(D) - 1]

    print(answer.upper())
