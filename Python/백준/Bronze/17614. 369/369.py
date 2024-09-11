N = int(input())
M = [
    str(i)
    for i in range(1, N + 1)
    if any(["3" in str(i), "6" in str(i), "9" in str(i)])
]
M = sum([len([i for i in x if i in "369"]) for x in M])
print(M)