from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import QLineF, QPointF, QRectF
import math
from src.utility import *


BLACK_PEN = QPen(QColor(0, 0, 0), 3)


def draw_to_pdm(painter, points, shift):
    """
    Draws a list of points shifted horizontally by `shift` pixels.

    Parameters:
        painter : QPainter             # The active painter from your MainWindow
        points  : list[(x, y)]         # The stored points from input
        shift   : int                  # How much to shift points to the right
    """


    if not points:
        return

    painter.setPen(BLACK_PEN)

    # Draw segments between consecutive points
    MAX_DISTANCE = 25  # maximum allowed distance in pixels

    for i in range(1, len(points)):
        x1, y1 = points[i - 1]
        x2, y2 = points[i]

        # Compute Euclidean distance
        dist = math.hypot(x2 - x1, y2 - y1)

        if dist > MAX_DISTANCE:
            continue

        # painter.drawLine(QLineF(x1 + shift, y1, x2 + shift, y2))
        painter.drawPoint(QPointF(x1 + shift, y1))




def points_to_pdm(painter, points, shift, center, radius):

    if not points:
        return

    painter.setPen(BLACK_PEN)

    for i in range(1, len(points)):
        if i % 2 == 1:
            x1, y1 = points[i]
            x2, y2 = points[i - 1]
            painter.drawLine(QLineF(x1 + shift, y1, x2 + shift, y2))
            painter.drawLine(QLineF(x1, y1, x2, y2))

            new_center, new_radius = orthogonal_circle_through_two_points(center, radius, points[i - 1], points[i])

            # angle_between_points(new_center, points[i - 1], points[i])
            #
            # rect = QRectF(
            #     new_center.x() - new_radius,
            #     new_center.y() - new_radius,
            #     2 * new_radius,
            #     2 * new_radius
            # )
            #
            # start_angle16 = int(angle_from_center(new_center, points[i - 1]) * 16)
            # span_angle16 = int(angle_between_points(new_center, points[i - 1], points[i]) * 16)
            #
            # # PyQt draws clockwise, so negate both to go CCW
            # painter.drawArc(rect, -start_angle16, -span_angle16)

            # Draw circle with horizontal shift
            center_with_shift = QPointF(new_center.x() + shift, new_center.y())
            painter.drawEllipse(center_with_shift, new_radius, new_radius)



