import sys
from collections import deque

input = sys.stdin.readline


def read():
    N, K = map(int, input().strip().split())
    D = [0] + list(map(int, input().strip().split()))

    M = {x: [] for x in range(1, N + 1)}
    __edges = [0 for _ in range(N + 1)]
    for _ in range(K):
        X, Y = map(int, input().strip().split())

        if M.get(X) is None:
            M[X] = [Y]
        else:
            M[X].append(Y)

        __edges[Y] += 1

    __times = [0 for _ in range(N + 1)]
    __queue = deque()
    for i in range(1, N + 1):
        if __edges[i] == 0:
            __times[i] = D[i]
            __queue.append(i)

    W = int(input())

    return D, M, W, __edges, __queue, __times


if __name__ == "__main__":
    T = int(input())

    for _ in range(T):
        D, M, W, edges, queue, times = read()

        while queue:
            __node = queue.popleft()
            __time = times[__node]

            for v in M[__node]:
                edges[v] -= 1

                if not edges[v]:
                    queue.append(v)

                times[v] = max(times[v], __time + D[v])

        print(times[W])
