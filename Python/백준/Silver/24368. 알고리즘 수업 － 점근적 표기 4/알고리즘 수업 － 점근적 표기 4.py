a2, a1, a0 = map(int, input().strip().split())
c = int(input())
n0 = int(input())

if c == a2:
    print(int(a1 <= 0 and (c - a2) * (n0**2) - (a1 * n0) - a0 >= 0))
elif a2 > c:
    print(0)
elif a1 > 2 * (c - a2) * n0:
    print(int((a1**2) + 4 * a0 * (c - a2) <= 0))
else:
    print(int((c - a2) * (n0**2) - (a1 * n0) - a0 >= 0))
