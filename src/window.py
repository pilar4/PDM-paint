from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QPixmap, QPainterPath
from PyQt6.QtCore import QRectF, QLineF, Qt
import PyQt6.QtGui as QtGui
import sys
from src.calculate_points import draw_to_pdm

width = 1920
height = 1080

BLACK_PEN = QPen(QColor(0, 0, 0), 3)


# Base class draws background and separator line
class PaintBase(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(255, 255, 255))
        painter.setPen(BLACK_PEN)
        painter.drawLine(QLineF(width / 2, 0, width / 2, height))


class MainWindow(PaintBase):
    def __init__(self):
        super().__init__()
        self.last_x, self.last_y = None, None

        # Transparent canvases
        self.canvas_euler = QPixmap(width, height)
        self.canvas_euler.fill(Qt.GlobalColor.transparent)

        self.canvas_pdm = QPixmap(width, height)
        self.canvas_pdm.fill(Qt.GlobalColor.transparent)

        # Geometry
        self.radius = (width / 2) - (width / 10)
        self.euler_center = (width / 4, height / 2)
        self.pdm_center = ((width / 4) * 3, height / 2)

        # Circular areas
        self.euler_path = QtGui.QPainterPath()
        self.euler_path.addEllipse(
            self.euler_center[0] - self.radius / 2,
            self.euler_center[1] - self.radius / 2,
            self.radius,
            self.radius
        )
        self.pdm_path = QtGui.QPainterPath()
        self.pdm_path.addEllipse(
            self.pdm_center[0] - self.radius / 2,
            self.pdm_center[1] - self.radius / 2,
            self.radius,
            self.radius
        )

        # Store all drawn points here
        self.euler_points = []  # [(x1, y1), (x2, y2), ...]
        self.pdm_points = []    # same for the right circle

    # ------------------------------
    # Mouse handling
    # ------------------------------
    def mouseMoveEvent(self, e):
        x, y = e.position().x(), e.position().y()

        if self.last_x is None:
            self.last_x, self.last_y = x, y
            return

        # Determine drawing target
        if self.euler_path.contains(e.position()):
            target_canvas = self.canvas_euler
            points_list = self.euler_points
        elif self.pdm_path.contains(e.position()):
            target_canvas = self.canvas_pdm
            points_list = self.pdm_points
        else:
            self.last_x, self.last_y = x, y
            return

        # All points list
        points_list.append((x, y))

        # Draw line
        painter = QtGui.QPainter(target_canvas)
        painter.setPen(BLACK_PEN)
        painter.drawLine(QLineF(self.last_x, self.last_y, x, y))
        painter.end()

        self.last_x, self.last_y = x, y
        self.update()

    def mouseReleaseEvent(self, e):
        self.last_x = self.last_y = None


    # ------------------------------
    # Drawing functions
    # ------------------------------
    def paint_euclidean(self, painter):
        painter.setPen(BLACK_PEN)
        radius = self.radius
        x = (width / 4) - (radius / 2)
        y = (height / 2) - (radius / 2)

        # text
        text_size = width // 55
        painter.setFont(QFont("Consolas", text_size))
        text_rect = QRectF(x, y - (height / 12), radius, text_size * 2)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, "Euclidean plane")

        # circle + square
        circle_rect = QRectF(x, y, radius, radius)
        painter.drawEllipse(circle_rect)
        painter.drawRect(circle_rect)

    def paint_pdm(self, painter):
        painter.setPen(BLACK_PEN)
        radius = self.radius
        x = ((width / 4) * 3) - (radius / 2)
        y = (height / 2) - (radius / 2)

        # text
        text_size = width // 55
        painter.setFont(QFont("Consolas", text_size))
        text_rect = QRectF(x, y - (height / 12), radius, text_size * 2)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, "Poincaré disk plane")

        # circle
        circle_rect = QRectF(x, y, radius, radius)
        painter.drawEllipse(circle_rect)

    # ------------------------------
    # Paint event
    # ------------------------------
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw static components
        self.paint_euclidean(painter)
        self.paint_pdm(painter)

        # Draw the canvases
        painter.drawPixmap(0, 0, self.canvas_euler)
        painter.drawPixmap(0, 0, self.canvas_pdm)

        draw_to_pdm(painter, euler_points(), shift=960)

        painter.end()






app = QApplication(sys.argv)
window = MainWindow()

def draw():

    window.resize(width, height)
    window.show()
    app.exec()



def euler_points():
    return window.euler_points
def pdm_points():
    return window.pdm_points
