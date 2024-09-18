import sys


def read():
    input = sys.stdin.readline

    T = int(input())
    TC = []

    for _ in range(T):
        case = []

        while True:
            i = int(input())

            if i == 0:
                break
            else:
                case.append(i)

        case.sort(reverse=True)
        TC.append(case)

    return T, TC


def cal_price(n, i):
    return 2 * (n**i)


if __name__ == "__main__":
    T, TC = read()
    SEED = 5 * 1e6

    for case in TC:
        total_price = sum([cal_price(n, i + 1) for i, n in enumerate(case)])

        print(total_price if total_price <= SEED else "Too expensive")
