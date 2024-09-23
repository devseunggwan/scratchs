from copy import deepcopy


def read():
    N = int(input())
    M = [list(map(int, input().strip().split())) for _ in range(N)]

    return N, M


def rotate_clockwise(matrix):
    return [list(row) for row in zip(*matrix[::-1])]


def rotate_counterclockwise(matrix):
    return [list(row) for row in zip(*matrix)][::-1]


def trasnpose(M, position):
    if position == "up":
        return rotate_counterclockwise(M)
    elif position == "bottom":
        return rotate_clockwise(M)
    elif position == "left":
        return M
    elif position == "right":
        return [row[::-1] for row in M]


def detranspose(M, position):
    if position == "up":
        return rotate_clockwise(M)
    elif position == "bottom":
        return rotate_counterclockwise(M)
    elif position == "left":
        return M
    elif position == "right":
        return [row[::-1] for row in M]


def merge(N, M):
    for i in range(N):
        for curr in range(N - 1):
            while M[i][curr] == 0:
                if sum(M[i][curr:]) == 0:
                    break

                M[i].pop(curr)
                M[i].append(0)

            while M[i][curr + 1] == 0:
                if sum(M[i][(curr + 1) :]) == 0:
                    break

                M[i].pop(curr + 1)
                M[i].append(0)

            if M[i][curr] == M[i][curr + 1] and M[i][curr] != 0:
                M[i][curr] = M[i][curr] + M[i][curr + 1]
                M[i].pop(curr + 1)
                M[i].append(0)

    return M


def process(N, M, position):
    POSITIONS = ["up", "bottom", "left", "right"]

    M = trasnpose(M, position=POSITIONS[position])
    M = merge(N, M)
    M = detranspose(M, position=POSITIONS[position])

    return M


def dfs(depth, M, proc):
    global N, answer

    if depth == 5:
        answer = max(answer, max([max(x) for x in M]))
        return

    for position in range(4):
        __M = deepcopy(M)
        __M = process(N, __M, position)
        dfs(depth + 1, __M, proc + [position])


if __name__ == "__main__":
    N, M = read()
    answer = 0
    dfs(0, M, [])

    print(answer)
