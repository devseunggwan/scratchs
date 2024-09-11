N = int(input())
print(
    len(
        [
            str(i)
            for i in range(1, N + 1)
            if any(["3" in str(i), "6" in str(i), "9" in str(i)])
        ]
    )
)
