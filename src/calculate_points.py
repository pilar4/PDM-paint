from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import QLineF, QPointF, QRectF
import math
from src.utility import *


BLACK_PEN = QPen(QColor(0, 0, 0), 3)


def draw_to_pdm(painter, points, shift):


    if not points:
        return

    painter.setPen(BLACK_PEN)

    MAX_DISTANCE = 25  # maximum allowed distance in pixels

    for i in range(1, len(points)):
        x1, y1 = points[i - 1]
        x2, y2 = points[i]


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
            # painter.drawLine(QLineF(x1 + shift, y1, x2 + shift, y2))
            painter.drawLine(QLineF(x1, y1, x2, y2))

            new_center, new_radius = orthogonal_circle_through_two_points(center, radius, points[i - 1], points[i])

            rect = QRectF(
                (new_center.x() + shift) - new_radius,
                new_center.y() - new_radius,
                2 * new_radius,
                2 * new_radius
            )

            start_angle = angle_from_center(new_center, points[i - 1])
            span_angle = angle_between_points(new_center, points[i - 1], points[i])

            # when painting clockwise span angle is bigger than 180 due to how i do math in utility
            # so its critical to flip the angle (to avoid drawing full circle EXCEPT the arc wanted
            if span_angle > 180:
                span_angle -= 360

            start_angle16 = int(start_angle * 16)
            span_angle16 = int(span_angle * 16)

            painter.drawArc(rect, -start_angle16, -span_angle16)


