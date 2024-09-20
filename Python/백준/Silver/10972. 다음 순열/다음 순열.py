import sys


def read():
    input = sys.stdin.readline

    N = int(input())
    M = list(map(int, input().strip().split()))

    return N, M


def get_idx(N: list[int]) -> int:
    for idx in range(N - 1, -1, -1):
        if M[idx] > M[idx - 1]:
            break

    idx = idx - 1

    return idx


def get_curr(N: list[int], idx: int) -> int:
    for curr in range(N - 1, idx, -1):
        if M[idx] < M[curr]:
            break

    return curr


if __name__ == "__main__":
    N, M = read()

    idx = get_idx(N)
    if idx == -1:
        print(-1)
        exit()

    curr = get_curr(N, idx)

    M[idx], M[curr] = M[curr], M[idx]
    M[idx + 1 :] = sorted(M[idx + 1 :])

    print(*M)
