def read():
    N = int(input())

    TC = [sorted(map(int, input().strip().split())) for _ in range(N)]

    return TC


def is_vaild(case):
    return case[0] ** 2 + case[1] ** 2 == case[2] ** 2


if __name__ == "__main__":
    TC = read()

    for idx, case in enumerate(TC):
        print(f"Scenario #{idx + 1}:")
        print("yes" if is_vaild(case) else "no")
        print("")
