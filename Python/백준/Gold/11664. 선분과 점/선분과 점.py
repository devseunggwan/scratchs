import math


def get_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def point_to_segment_distance(px, py, pz, ax, ay, az, bx, by, bz):
    abx, aby, abz = bx - ax, by - ay, bz - az
    apx, apy, apz = px - ax, py - ay, pz - az

    ab_len_sg = abx**2 + aby**2 + abz**2

    t = (apx * abx + apy * aby + apz * abz) / ab_len_sg

    if t < 0:
        return get_distance(px, py, pz, ax, ay, az)
    elif t > 1:
        return get_distance(px, py, pz, bx, by, bz)
    else:
        dx, dy, dz = ax + t * abx, ay + t * aby, az + t * abz

        return get_distance(px, py, pz, dx, dy, dz)


if __name__ == "__main__":
    Ax, Ay, Az, Bx, By, Bz, Cx, Cy, Cz = map(int, input().strip().split())

    distance = point_to_segment_distance(Cx, Cy, Cz, Ax, Ay, Az, Bx, By, Bz)

    print("%.10f" % distance)
