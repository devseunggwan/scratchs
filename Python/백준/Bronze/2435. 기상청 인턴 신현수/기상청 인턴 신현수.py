N, K = map(int, input().strip().split())
T = list(map(int, input().strip().split()))
print(max([sum(T[i : i + K]) for i in range(N - K + 1)]))
