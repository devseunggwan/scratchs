import sys


def read():
    input = sys.stdin.readline

    N = int(input())
    M = [[i] + list(map(int, input().strip().split())) for i in range(1, N + 1)]

    return N, M


def dfs(P, x, y, color, cnt, direction):
    __map = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

    __j, __i = __map[direction]
    if P[__j + y][__i + x] == color:
        cnt = dfs(
            P,
            __i + x,
            __j + y,
            color,
            cnt + 1,
            direction,
        )

    return cnt


def solve(N, M):
    is_win = 0

    P = [[0 for _ in range(22)] for _ in range(22)]

    for idx, x, y in M:
        P[y][x] = 1 if idx % 2 else 2

        for j in range(1, 20):
            for i in range(1, 20):
                if P[j][i]:
                    for d in range(4):
                        is_win = dfs(P, i, j, P[j][i], 0, d) + dfs(
                            P, i, j, P[j][i], 0, -(d + 1)
                        )
                        if is_win == 4:
                            return idx
    return -1


if __name__ == "__main__":
    N, M = read()
    print(solve(N, M))
