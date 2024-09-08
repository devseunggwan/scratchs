def read():
    M = input()
    M = [False] + [True if x == "Y" else False for x in M]

    return M


if __name__ == "__main__":
    M = read()
    answer = 0

    for idx, flag in enumerate(M):
        if flag:
            answer += 1

            for i in range(idx, len(M), idx):
                M[i] = not M[i]

    print(answer)
