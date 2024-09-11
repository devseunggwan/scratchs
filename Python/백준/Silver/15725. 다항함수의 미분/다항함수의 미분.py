S = input()
idx = -1


for i in range(len(S)):
    if S[i] == "x":
        idx = i

if idx == -1:
    print(0)
elif idx == 0:
    print(1)
elif (idx == 1) & (S[0] == "-"):
    print(-1)
else:
    print(S[:idx])
