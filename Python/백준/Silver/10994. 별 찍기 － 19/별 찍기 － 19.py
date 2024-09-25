from collections import deque

N = int(input())
answer = deque(["*"])

for i in range(N - 1):
    # 기존 도형 업데이트
    for j in range(len(answer)):
        answer[j] = f"* {answer[j]} *"

    t1 = f"*{' ' * ((4 * i) + 3)}*"
    answer.appendleft(t1)
    answer.append(t1)

    t2 = "*" * (1 + (4 * (i + 1)))
    answer.appendleft(t2)
    answer.append(t2)

for row in answer:
    print(row)
