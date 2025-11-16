from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import QLineF, QPointF, QRectF
import math

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




def points_to_pdm(painter, points, shift):

    if not points:
        return

    painter.setPen(BLACK_PEN)

    for i in range(1, len(points)):
        if i%2==1:
            x1, y1 = points[i]
            x2, y2 = points[i - 1]
            painter.drawLine(QLineF(x1 + shift, y1, x2 + shift, y2))

            # Draws lines on Euclidean from points
            painter.drawLine(QLineF(x1, y1, x2, y2))

