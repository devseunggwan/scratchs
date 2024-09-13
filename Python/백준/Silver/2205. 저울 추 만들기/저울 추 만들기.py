import math
from collections import deque


def get_mess(i, masses):
    for mass in range(N, 0, -1):
        if math.log2(i + mass).is_integer() and not masses[mass]:
            masses[mass] = 1
            break

    return mass


if __name__ == "__main__":
    N = int(input())
    masses = [0 for _ in range(N + 1)]
    answer = deque()

    for i in range(N, 0, -1):
        mass = get_mess(i, masses)
        answer.appendleft(mass)

    [print(x) for x in answer]
