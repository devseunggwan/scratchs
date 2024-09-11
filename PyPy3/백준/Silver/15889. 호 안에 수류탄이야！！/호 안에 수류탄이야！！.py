import sys
from collections import deque


def read():
    input = sys.stdin.readline

    N = int(input())
    X = list(map(int, input().strip().split()))
    R = list(map(int, input().strip().split())) + [0]

    M = [(loc, cost) for loc, cost in zip(X, R)]

    return N, M


if __name__ == "__main__":
    N, M = read()
    queue = deque([0])

    answer = "엄마 나 전역 늦어질 것 같아"

    while queue:
        idx = queue.popleft()
        members = []

        if idx + 1 == N:
            answer = "권병장님, 중대장님이 찾으십니다"
            break

        for i in range(idx + 1, N):
            if M[i][0] - M[idx][0] <= M[idx][1]:
                members.append((i, M[i][1] + M[i][0] - M[idx][0]))

        if members:
            queue.append(max(members, key=lambda x: x[1])[0])

    print(answer)
