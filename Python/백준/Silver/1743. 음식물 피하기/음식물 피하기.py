import sys
from collections import deque


def read():
    input = sys.stdin.readline

    N, M, K = map(int, input().strip().split())

    __map = [[0 for _ in range(M)] for _ in range(N)]
    __visits = [[0 for _ in range(M)] for _ in range(N)]
    __xy = deque([])

    for _ in range(K):
        r, c = map(int, input().strip().split())
        __xy.append((r - 1, c - 1))

        __map[r - 1][c - 1] = 1

    return N, M, __map, __visits, __xy


def bfs(N, M, __map, __visits, r, c):
    route = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    cnt = 1
    __visits[r][c] = 1
    __queue = deque([(r, c)])

    while __queue:
        __r, __c = __queue.popleft()

        for i, j in route:
            if not ((0 <= __r + i < N) and (0 <= __c + j < M)):
                continue

            if __map[__r + i][__c + j] and not __visits[__r + i][__c + j]:
                cnt += 1
                __visits[__r + i][__c + j] = 1
                __queue.append((__r + i, __c + j))

    return cnt, __visits


if __name__ == "__main__":
    N, M, __map, __visits, __rc = read()
    answer = 1

    while __rc:
        __r, __c = __rc.popleft()
        if __visits[__r][__c]:
            continue

        __cnt, __visits = bfs(N, M, __map, __visits, __r, __c)
        answer = max(answer, __cnt)

    print(answer)
