import math
from PyQt6.QtCore import QPointF

def orthogonal_circle_through_two_points(O1, R1, P, Q):
    x1, y1 = O1
    px, py = P
    qx, qy = Q

    mx = (px + qx) / 2
    my = (py + qy) / 2

    dx = qx - px
    dy = qy - py
    d = math.hypot(dx, dy)

    if d == 0:
        raise ValueError("P and Q must be different points. (painted the same point twice)")

    nx = -dy / d
    ny =  dx / d

    ox = x1 - mx
    oy = y1 - my
    D = (d*d)/4

    A = -2*(ox*nx + oy*ny)
    B = ox*ox + oy*oy - R1*R1 - D

    if A == 0:
        raise ValueError("No orthogonal circle exists with these constraints.")

    t = -B / A

    cx = mx + t*nx
    cy = my + t*ny

    R2 = math.hypot(cx - px, cy - py)

    return QPointF(cx, cy), R2


def angle_from_center(center, point) -> float:

    dx = point[0] - center.x()
    dy = point[1] - center.y()
    return math.degrees(math.atan2(dy, dx))


def angle_between_points(center, p, q) -> float:

    start = angle_from_center(center, p)
    end = angle_from_center(center, q)
    span = end - start
    if span < 0:
        span += 360
    return span

