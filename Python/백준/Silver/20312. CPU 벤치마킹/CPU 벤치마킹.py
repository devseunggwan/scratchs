import sys


def read():
    input = sys.stdin.readline

    N = int(input())
    M = list(map(int, input().strip().split()))

    return N, M


if __name__ == "__main__":
    N, M = read()
    MOD = 1000000007

    curr = 0
    answer = 0

    for i in range(N - 1):
        curr = ((curr + 1) * M[i]) % MOD
        answer = (answer + curr) % MOD

    print(int(answer))
