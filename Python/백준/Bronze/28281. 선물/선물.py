N, X = map(int, input().strip().split())
A = map(int, input().strip().split())
A = list(map(lambda x: x * X, A))
print(min([A[i] + A[i + 1] for i in range(N - 1)]))
