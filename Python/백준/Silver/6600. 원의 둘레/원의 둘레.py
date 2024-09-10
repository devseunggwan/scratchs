import math
import sys

while True:
    try:
        x1, y1, x2, y2, x3, y3 = map(float, sys.stdin.readline().strip().split())
    except Exception:
        break

    d = math.hypot(x3 - x2, y3 - y2)
    ax = x2 - x1
    ay = y2 - y1
    bx = x3 - x1
    by = y3 - y1

    theta = math.acos((ax * bx + ay * by) / (math.hypot(ax, ay) * math.hypot(bx, by)))
    print("%.2f" % (d / math.sin(theta) * math.pi))
