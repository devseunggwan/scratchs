def read():
    N = int(input())
    A = list(map(int, input().strip().split()))

    return N, A


def is_ascending(N: int, A: list[int]) -> bool:
    if N == 1:
        return True

    return len(set([A[i + 1] - A[i] for i in range(N - 1)])) == 1


def n_is_one(N: int, A: list[int]):
    if A[0] == 0:
        return [1], [-1]
    else:
        return [A[0] * 2], [-A[0]]


def n_is_many(N: int, A: list[int]):
    B, C = [b * 2 for b in A], [-c for c in A]

    return B, C


if __name__ == "__main__":
    N, A = read()

    flag = is_ascending(N, A)
    print("YES" if flag else "NO")

    if flag:
        B, C = n_is_one(N, A) if N == 1 else n_is_many(N, A)

        print(" ".join(map(str, B)))
        print(" ".join(map(str, C)))
