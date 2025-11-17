import math
from PyQt6.QtCore import QPointF

def orthogonal_circle_through_two_points(O1, R1, P, Q):
    # Unpack points
    x1, y1 = O1
    px, py = P
    qx, qy = Q

    # Midpoint of PQ
    mx = (px + qx) / 2
    my = (py + qy) / 2

    # PQ vector and length
    dx = qx - px
    dy = qy - py
    d = math.hypot(dx, dy)

    if d == 0:
        raise ValueError("P and Q must be different points.")

    # Normalized perpendicular vector to PQ
    nx = -dy / d
    ny =  dx / d

    # Distance from midpoint to center of new circle is unknown t.
    # Solve for t via orthogonality.

    # left side of orthogonality:
    # |O1O2|^2 = R1^2 + R2^2
    # R2 = sqrt(t^2 + (d/2)^2)
    # O2 = M + t*n

    # Expand equation:
    # |O1 - (M+t*n)|^2 = R1^2 + t^2 + (d/2)^2

    # Define useful values
    ox = x1 - mx
    oy = y1 - my
    D = (d*d)/4

    # Quadratic in t:
    # (ox - t*nx)^2 + (oy - t*ny)^2 = R1^2 + t^2 + D
    #
    # Expand:
    # ox^2 + oy^2 -2*t*(ox*nx + oy*ny) + t^2 = R1^2 + t^2 + D
    #
    # t^2 cancels → linear equation in t

    A = -2*(ox*nx + oy*ny)
    B = ox*ox + oy*oy - R1*R1 - D

    # A*t + B = 0 → t = -B/A
    if A == 0:
        raise ValueError("No orthogonal circle exists with these constraints.")

    t = -B / A

    # Compute center of orthogonal circle
    cx = mx + t*nx
    cy = my + t*ny

    # Compute its radius
    R2 = math.hypot(cx - px, cy - py)

    return QPointF(cx, cy), R2



import math
from PyQt6.QtCore import QPointF

def angle_from_center(center, point) -> float:
    """
    Returns the angle (in degrees) from the horizontal axis to the point,
    measured counterclockwise from the center.
    """
    dx = point[0] - center.x()
    dy = point[1] - center.y()
    return math.degrees(math.atan2(dy, dx))


def angle_between_points(center, p, q) -> float:
    """
    Returns the angle (in degrees) from point p to point q, relative to center.
    Always returns a positive angle in range [0, 360).
    """
    start = angle_from_center(center, p)
    end = angle_from_center(center, q)
    span = end - start
    if span < 0:
        span += 360
    return span

