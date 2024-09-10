import sys
from itertools import combinations


def read():
    input = sys.stdin.readline

    N = int(input())
    M = [list(map(float, input().strip().split())) for _ in range(N)]

    return N, M


def euclidian_distance(a, b):
    return (((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2)) ** 0.5


def find(parent, x):
    while parent[x] != x:
        x = parent[x]

    return x


def union(parent, s, t):
    s = find(parent, s)
    t = find(parent, t)

    parent[max(s, t)] = min(s, t)


if __name__ == "__main__":
    N, M = read()
    parent = [i for i in range(N + 1)]
    answer = []

    V = combinations(range(N), 2)
    M = sorted(
        [(i, j, euclidian_distance(M[i], M[j])) for i, j in V], key=lambda x: x[2]
    )

    for s, t, cost in M:
        if find(parent, s) != find(parent, t):
            answer.append(cost)
            union(parent, s, t)

        if len(answer) - 1 == N:
            break

    print("%.2f" % sum(answer))
