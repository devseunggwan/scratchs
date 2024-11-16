import sys


def read():
    input = sys.stdin.readline
    cases = []

    while True:
        p = int(input().strip())

        if p == 0:
            break

        M = [list(map(int, input().strip().split())) for _ in range(p)]
        cases.append(M)

    return cases


def solve(M):
    M = sorted(M, key=lambda x: x[1] - x[0])
    time_table = [0] * 25

    for s, e in M:
        for i in range(s, e):
            if time_table[i] < 2:
                time_table[i] += 1
                break

    return sum(time_table)


if __name__ == "__main__":
    cases = read()

    for d, M in enumerate(cases):
        n = solve(M)

        print(f"On day {d + 1} Emma can attend as many as {n} parties.")
