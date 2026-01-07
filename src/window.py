from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QPixmap, QPainterPath
from PyQt6.QtCore import QRectF, QLineF, Qt, QPointF
import PyQt6.QtGui as QtGui
import PyQt6.QtCore as QtCore
import sys
from src.calculate_points import draw_to_pdm
from src.calculate_points import points_to_pdm

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
        self.euler_points = []            # drag points
        self.pdm_points = []

        # Store click points here
        self.euler_click_points = []
        self.pdm_click_points = []

    # ------------------------------
    # Mouse handling
    # ------------------------------
    def mouseMoveEvent(self, e):
        # Only draw when dragging
        if not (e.buttons() & Qt.MouseButton.LeftButton):
            return

        x, y = e.position().x(), e.position().y()

        # Determine drawing target
        if self.euler_path.contains(e.position()):
            target_canvas = self.canvas_euler
            points_list = self.euler_points
        elif self.pdm_path.contains(e.position()):
            target_canvas = self.canvas_pdm
            points_list = self.pdm_points
        else:
            return

        # Save drag point
        points_list.append((x, y))

        # Draw a dot (not a line)
        painter = QtGui.QPainter(target_canvas)
        painter.setPen(BLACK_PEN)
        r = BLACK_PEN.width() / 2
        painter.drawEllipse(QtCore.QPointF(x, y), r, r)
        painter.end()

        self.update()

    def mousePressEvent(self, e):
        # Only respond to RIGHT-click (as in your last code)
        if e.button() != Qt.MouseButton.RightButton:
            return

        x, y = e.position().x(), e.position().y()

        # Determine drawing target
        if self.euler_path.contains(e.position()):
            target_canvas = self.canvas_euler
            points_list = self.euler_click_points   # NEW
        elif self.pdm_path.contains(e.position()):
            target_canvas = self.canvas_pdm
            points_list = self.pdm_click_points     # NEW
        else:
            return

        # Save click point
        points_list.append((x, y))

        # Draw dot
        painter = QtGui.QPainter(target_canvas)
        painter.setPen(BLACK_PEN)
        r = BLACK_PEN.width()
        painter.drawPoint(QtCore.QPointF(x, y))
        painter.end()

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
        rc = QRectF(x, y - (height / 12), radius*2.2, text_size)
        # painter.drawText(rc, Qt.AlignmentFlag.AlignCenter, "(press right click)")


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

        # Map Euclidean drag points to Poincaré (unchanged)
        draw_to_pdm(painter, euler_points(), shift=960)
        points_to_pdm(
            painter,
            euler_click_points(),
            shift=960,
            center=self.euler_center,
            radius=self.radius / 2
        )

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

# troubleshooting
def euler_click_points():
    return window.euler_click_points

def pdm_click_points():
    return window.pdm_click_points
