def prep_row(line):
    result = [int(line[i] == "-") for i in [1, 4, 7]]

    return result


def prep_col(line):
    result = [int(line[i] == "|") for i in [0, 3, 6, 9]]

    return result


if __name__ == "__main__":
    M = [input().strip() for _ in range(10)]
    row = []
    col = []

    answer = [0, 0]

    for i in range(10):
        if i % 3 == 0:
            __item = prep_row(M[i])
            answer[0] += 3 - sum(__item)

            row.append(__item)

        elif i % 3 == 1:
            __item = prep_col(M[i])
            answer[0] += 4 - sum(__item)

            col.append(__item)

    for i in range(3):
        for j in range(3):
            if all([row[i][j], row[i + 1][j], col[i][j], col[i][j + 1]]):
                answer[1] += 1

    for i in range(2):
        for j in range(2):
            if (
                sum(row[i][j : j + 2])
                + sum(row[i + 2][j : j + 2])
                + col[i][j]
                + col[i][j + 2]
                + col[i + 1][j]
                + col[i + 1][j + 2]
            ) == 8:
                answer[1] += 1

    if sum(row[0]) + sum(row[3]) + sum([x[0] + x[3] for x in col]) == 12:
        answer[1] += 1

    print(" ".join(map(str, answer)))
