def read() -> list[list[str]]:
    board = [list(map(int, list(input().strip()))) for _ in range(9)]
    zeros = []

    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                zeros.append((j, i))

    return board, zeros


def validate_row(board, y, num):
    for i in range(9):
        if board[y][i] == num:
            return False

    return True


def validate_col(board, x, num):
    for i in range(9):
        if board[i][x] == num:
            return False

    return True


def validate_square(board, x, y, num):
    __x, __y = (x // 3) * 3, (y // 3) * 3

    for i in range(__y, __y + 3):
        for j in range(__x, __x + 3):
            if board[i][j] == num:
                return False

    return True


def dfs(idx, board, zeros):
    if len(zeros) == idx:
        [print("".join(map(str, x))) for x in board]
        exit()

    x, y = zeros[idx]

    for num in range(1, 10):
        if (
            validate_row(board, y, num)
            and validate_col(board, x, num)
            and validate_square(board, x, y, num)
        ):
            board[y][x] = num
            dfs(idx + 1, board, zeros)
            board[y][x] = 0


if __name__ == "__main__":
    board, zeros = read()

    dfs(0, board, zeros)
