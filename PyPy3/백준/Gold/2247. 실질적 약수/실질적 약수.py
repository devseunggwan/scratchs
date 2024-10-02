def sod(N):
    result = 0

    for i in range(2, (N // 2) + 1):
        result += i * (N // i - 1) % 1_000_000

    result %= 1_000_000

    return result


if __name__ == "__main__":
    N = int(input())

    print(sod(N))
