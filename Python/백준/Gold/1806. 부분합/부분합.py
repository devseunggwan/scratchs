import sys
from itertools import accumulate


def read():
    input = sys.stdin.readline

    N, S = map(int, input().strip().split())
    M = list(map(int, input().strip().split()))
    M = [0] + list(accumulate(M))

    return N, S, M


if __name__ == "__main__":
    N, S, M = read()

    s, e = 0, 0
    answer = N + 1

    while s != N + 1 and e != N + 1:
        if M[e] - M[s] < S:
            e += 1
        else:
            answer = min(e - s, answer)
            s += 1

    print(answer if answer != N + 1 else 0)
