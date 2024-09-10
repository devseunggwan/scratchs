def read():
    V, E = map(int, input().strip().split())

    M = sorted(
        [list(map(int, input().strip().split())) for _ in range(E)], key=lambda x: x[2]
    )

    return V, E, M


def find(parent, x):
    while parent[x] != x:
        x = parent[x]

    return x


def union(parent, s, t):
    s = find(parent, s)
    t = find(parent, t)

    parent[max([s, t])] = min([s, t])


if __name__ == "__main__":
    V, E, M = read()
    parent = [i for i in range(V + 1)]
    answer = []

    for s, t, cost in M:
        if find(parent, s) != find(parent, t):
            answer.append(cost)
            union(parent=parent, s=s, t=t)

        if len(answer) - 1 == V:
            break

    print(sum(answer) - max(answer))
