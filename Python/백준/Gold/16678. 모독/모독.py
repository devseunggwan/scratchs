import sys


def read():
    input = sys.stdin.readline

    N = int(input().strip())
    M = sorted([int(input().strip()) for _ in range(N)])

    return N, M


if __name__ == "__main__":
    N, M = read()
    answer = 0
    pointer = 1

    for i in range(N):
        if M[i] == pointer:
            if i + 1 < N and M[i + 1] > M[i]:
                pointer += 1
        if M[i] > pointer:
            answer += M[i] - pointer
            pointer += 1

    print(answer)
