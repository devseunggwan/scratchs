import sys
from collections import deque


def read():
    input = sys.stdin.readline

    N, M = map(int, input().strip().split())
    M = [map(int, input().strip().split()) for _ in range(M)]

    return N, M


def get_graph(N, M):
    __graph = [[] for _ in range(N + 1)]
    __indegree = [0 for _ in range(N + 1)]

    for A, B in M:
        __graph[A].append(B)
        __indegree[B] += 1

    return __graph, __indegree


def topology_sort(graph, indegree):
    result = [0 for _ in range(len(indegree))]
    queue = deque()

    for i in range(1, len(indegree)):
        if indegree[i] == 0:
            queue.append(i)
            result[i] += 1

    while queue:
        node = queue.popleft()

        for child in graph[node]:
            indegree[child] -= 1

            if indegree[child] == 0:
                queue.append(child)

            result[child] = result[node] + 1

    return result


if __name__ == "__main__":
    N, M = read()
    graph, indegree = get_graph(N, M)
    answer = topology_sort(graph, indegree)

    print(" ".join(list(map(str, answer))[1:]))
