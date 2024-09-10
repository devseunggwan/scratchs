import math
import sys
from itertools import combinations


def read():
    input = sys.stdin.readline

    N, M = map(int, input().strip().split())

    X = [list(map(int, input().strip().split())) for _ in range(N)]
    Y = [list(map(int, input().strip().split())) for _ in range(M)]

    return N, M, X, Y


def euclidian_distance(a, b):
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))


def find(parent, x):
    while parent[x] != x:
        x = parent[x]

    return x


def union(parent, s, t):
    s = find(parent, s)
    t = find(parent, t)

    parent[max(s, t)] = min(s, t)


if __name__ == "__main__":
    N, M, X, Y = read()
    parent = [i for i in range(N + 1)]
    answer = []
    y_map = {}

    V = set(combinations(range(N), 2))
    V = sorted(
        [(i, j, euclidian_distance(X[i], X[j])) for i, j in V], key=lambda x: x[2]
    )

    Y = [(i - 1, j - 1, euclidian_distance(X[i - 1], X[j - 1])) for i, j in Y]

    for s, t, cost in Y:
        if find(parent, s) != find(parent, t):
            answer.append(0)
            y_map[f"{min(s, t)}_{max(s, t)}"] = 1
            union(parent, s, t)

    for s, t, cost in V:
        if (
            find(parent, s) != find(parent, t)
            and y_map.get(f"{min(s, t)}_{max(s, t)}") is None
        ):
            answer.append(cost)
            union(parent, s, t)

        if len(answer) - 1 == N:
            break

    print("%.2f" % sum(answer))
