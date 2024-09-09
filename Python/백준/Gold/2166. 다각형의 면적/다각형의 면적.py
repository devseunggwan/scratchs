import sys


def read():
    input = sys.stdin.readline

    N = int(input())
    M = [list(map(int, input().strip().split())) for _ in range(N)]

    return N, M


if __name__ == "__main__":
    answer = 0

    N, M = read()
    j = N - 1

    for i in range(N):
        x1, y1 = M[i]
        x2, y2 = M[j]

        answer += (x1 * y2) - (x2 * y1)
        j = i

    answer = abs(answer) / 2

    print(answer)
