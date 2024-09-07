import sys


def read():
    input = sys.stdin.readline

    TC = int(input())
    CASES = [
        (i + 1, int(input()), list(map(int, input().strip().split())))
        for i in range(TC)
    ]

    return TC, CASES


def game(case):
    while len(case) != 2:
        temp = [case[len(case) // 2] * 2] if len(case) % 2 == 1 else []
        case = [case[i] + case[-i - 1] for i in range(len(case) // 2)] + temp

    return case


if __name__ == "__main__":
    TC, CASES = read()

    for idx, N, case in CASES:
        if N == 2:
            alice, bob = case
        else:
            alice, bob = game(case)

        print(f"Case #{idx}: " + ("Alice" if alice > bob else "Bob"))
