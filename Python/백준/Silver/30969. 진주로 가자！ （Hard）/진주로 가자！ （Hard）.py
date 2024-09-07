import sys

if __name__ == "__main__":
    input = sys.stdin.readline

    N = int(input())
    M = {1001: 0}
    jinju = 0
    P = 0

    for _ in range(N):
        city, price = input().strip().split()
        price = int(price)

        if city == "jinju":
            jinju = price

        if price <= 1000:
            if M.get(price) is None:
                M[price] = 1
            else:
                M[price] += 1
        else:
            M[1001] += 1

    for key in M:
        if key > jinju:
            P += M[key]

    print(jinju)
    print(P)
