from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QPoint

from view.forms import MainForm, GridDataForm


class MainView(QMainWindow):    
    draw_line = False

    def __init__(self):
        super(MainView, self).__init__()
        self.ui = MainForm(self)
        self.grid = GridDataForm(self)

        self.init_UI()
        
    def init_UI(self):
        self.ui.DrawPushButton.clicked.connect(self.draw_line)
        
        self._hide_interface()
                
    def _hide_interface(self):
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        def _draw_grid():
            pen = QPen(Qt.black)
            pen.setWidth(1)
            painter.setPen(pen)

            # Draw the coordinate grid
            for x in range(self.grid.start_x, self.grid.start_x + self.grid.size + 1, self.grid.spacing):
                painter.drawLine(x, self.grid.start_y, x, self.grid.start_y + self.grid.size)

            for y in range(self.grid.start_y, self.grid.start_y + self.grid.size + 1, self.grid.spacing):
                painter.drawLine(self.grid.start_x, y, self.grid.start_x + self.grid.size, y)
        
            # Draw axis labels
            font = QFont("Arial", 15)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(self.grid.start_x - 15, self.grid.start_y + self.grid.size + 15, "0")
            painter.drawText(self.grid.start_x + self.grid.size // 2 - 5, self.grid.start_y + self.grid.size + 25, "X")
            painter.drawText(self.grid.start_x - 25, self.grid.start_y + self.grid.size // 2 - 5, "Y")

        _draw_grid()
        if self.draw_line:
            pen = QPen(Qt.red)
            pen.setWidth(2)
            painter.setPen(pen)

            for i in range(len(self.points) - 1):
                point1 = self.points[i] + QPoint(self.grid.start_x, self.grid.start_y)
                point2 = self.points[i + 1] + QPoint(self.grid.start_x, self.grid.start_y)
                painter.drawLine(point1, point2)
        self.draw_line = False

    def draw_line(self):
        self.draw_line = True
        self.update()
        print("Line drawed!")
    
    @property
    def points(self):
        x1 = self.ui.x1SpinBox.value() * self.grid.POINT_MULT
        y1 = self.grid.size - self.ui.y1SpinBox.value() * self.grid.POINT_MULT 
        x2 = self.ui.x2SpinBox.value() * self.grid.POINT_MULT
        y2 = self.grid.size - self.ui.y2SpinBox.value() * self.grid.POINT_MULT

        return (QPoint(x1, y1), QPoint(x2, y2))
