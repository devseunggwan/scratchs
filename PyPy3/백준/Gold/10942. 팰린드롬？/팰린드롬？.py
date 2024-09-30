import sys


def read():
    input = sys.stdin.readline

    N = int(input())
    BOARD = list(map(int, input().strip().split()))
    Q = int(input())
    M = [list(map(int, input().strip().split())) for _ in range(Q)]

    DP = [[False for _ in range(N)] for _ in range(N)]

    for margin in range(N):
        for start in range(N):
            end = start + margin

            if end >= N:
                break

            if margin == 0:
                DP[start][end] = True
            elif margin == 1 and BOARD[start] == BOARD[end]:
                DP[start][end] = True
            elif BOARD[start] == BOARD[end] and DP[start + 1][end - 1]:
                DP[start][end] = True

    return M, DP


if __name__ == "__main__":
    M, DP = read()

    for S, E in M:
        print(int(DP[S - 1][E - 1]))
