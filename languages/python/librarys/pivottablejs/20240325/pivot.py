import duckdb
from pivottablejs import pivot_ui


if __name__ == "__main__":
    js = duckdb.query('SELECT * FROM "sample.json"')
    pivot_ui(js.df())
