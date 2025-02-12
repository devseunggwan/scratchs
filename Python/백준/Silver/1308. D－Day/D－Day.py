from datetime import datetime


def read():
    start_date = datetime(*list(map(int, input().strip().split())))
    end_date = datetime(*list(map(int, input().strip().split())))

    return start_date, end_date


def is_gg(start_date: datetime, end_date: datetime):
    if end_date.year - start_date.year > 1000:
        return True

    if all(
        [
            end_date.year - start_date.year == 1000,
            end_date.month - start_date.month >= 0,
            end_date.day - start_date.day >= 0
        ]
    ):
        return True

    return False



if __name__ == "__main__":
    start_date, end_date = read()

    if is_gg(start_date, end_date):
        print("gg")
    else:
        print(f"D-{(end_date - start_date).days}")
