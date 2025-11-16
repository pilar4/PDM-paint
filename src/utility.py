import math

from PyQt6.QtCore import QPointF


def orthogonal_circle(c1, r1, p1, q1):
    """
    Calculate the circle (center, radius) orthogonal to circle1
    that passes through points p1 and q1.

    Parameters:
        c1: tuple (x1, y1) - center of first circle
        r1: radius of first circle
        p1: tuple (x, y) - first point
        q1: tuple (x, y) - second point

    Returns:
        (c2, r2) - center and radius of orthogonal circle
    """
    x1, y1 = c1
    xp, yp = p1
    xq, yq = q1

    # Vector between points
    dx = xq - xp
    dy = yq - yp

    # Midpoint
    mx = (xp + xq)/2
    my = (yp + yq)/2

    # Perpendicular vector
    perp_dx = -dy
    perp_dy = dx

    # Function for r2^2 from orthogonality
    # Let c2 = (mx + t*perp_dx, my + t*perp_dy)
    # Then |c2 - p1|^2 = r2^2
    # And |c2 - c1|^2 = r1^2 + r2^2
    # Substitute r2^2 = |c2 - p1|^2 into second equation
    # Solve for t

    # Components
    a = perp_dx
    b = perp_dy
    cx = mx - x1
    cy = my - y1
    px = mx - xp
    py = my - yp

    # Quadratic coefficients for t
    A = a**2 + b**2
    B = 2*(a*cx + b*cy - a*px - b*py)
    C = cx**2 + cy**2 - (px**2 + py**2) - r1**2

    discriminant = B**2 - 4*A*C
    if discriminant < 0:
        raise ValueError("No real solution for orthogonal circle")

    sqrtD = math.sqrt(discriminant)
    t1 = (-B + sqrtD)/(2*A)
    t2 = (-B - sqrtD)/(2*A)

    # Compute centers
    c2_1 = (mx + t1*perp_dx, my + t1*perp_dy)
    c2_2 = (mx + t2*perp_dx, my + t2*perp_dy)

    # Choose the center that is "closer" to the points (inside unit circle usually)
    r2_1 = math.hypot(c2_1[0]-xp, c2_1[1]-yp)
    r2_2 = math.hypot(c2_2[0]-xp, c2_2[1]-yp)

    # Return one solution (you can choose other if needed)
    return (c2_1, r2_1)


c1 = (0, 0)
r1 = 1
p1 = (0.5, 0.2)
q1 = (-0.3, 0.4)

center, radius = orthogonal_circle(c1, r1, p1, q1)
print("Orthogonal circle center:", center)
print("Radius:", radius)
