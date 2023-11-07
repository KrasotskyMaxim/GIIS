from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QFont, QColor
from PyQt5.QtCore import Qt

from view.forms import MainForm, GridDataForm


class MainView(QWidget):
    LABLE_FONT = "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">{name}</span></p></body></html>"
    draw_line_switcher = False
    draw_circles_switcher = False

    def __init__(self):
        super(MainView, self).__init__()
        self.ui = MainForm(self)
        self.grid = GridDataForm(self)
        self.paint_model = None
        self.cache_points = []
        self.cache_saturation = []
        
        self.init_UI()
        
    def init_UI(self):
        self.ui.DrawPushButton.clicked.connect(self.draw_line)
        self.ui.LineManagerComboBox.currentIndexChanged.connect(self.prepare_circles_mode)
        
        self._hide_interface()
    
    def _hide_interface(self):
        pass
    
    def prepare_slines(self):
        draw_line_switcher = True
        draw_circles_switcher = False

        self.ui.LineManagerComboBox.setItemText(0, "CDA")
        self.ui.LineManagerComboBox.setItemText(1, "Brazenhem")
        self.ui.LineManagerComboBox.setItemText(2, "By")
        
        self.ui.x1Label.setText(self.LABLE_FONT.format(name="X1"))
        self.ui.y1Label.setText(self.LABLE_FONT.format(name="Y1"))
        self.ui.x2Label.setText(self.LABLE_FONT.format(name="X2"))
        self.ui.y2Label.setText(self.LABLE_FONT.format(name="Y2"))

        self.ui.x1Label.show()
        self.ui.y1Label.show()
        self.ui.x2Label.show()
        self.ui.y2Label.show()
        
        self.ui.x1SpinBox.show()
        self.ui.y1SpinBox.show()
        self.ui.x2SpinBox.show()
        self.ui.y2SpinBox.show()
        
    def prepare_circles(self):
        self.draw_line_switcher = False
        self.draw_circles_switcher = True

        self.ui.LineManagerComboBox.setItemText(0, "Circle")
        self.ui.LineManagerComboBox.setItemText(1, "Ellipse")
        self.ui.LineManagerComboBox.setItemText(2, "Hyperball")
        self.ui.LineManagerComboBox.setItemText(2, "Paraball")
        
        # circle by default
        self.ui.x1Label.setText(self.LABLE_FONT.format(name="X"))
        self.ui.y1Label.setText(self.LABLE_FONT.format(name="Y"))
        self.ui.x2Label.setText(self.LABLE_FONT.format(name="R"))
        
        self.ui.y2Label.hide()
        self.ui.y2SpinBox.hide()
    
        self.ui.x1Label.show()
        self.ui.y1Label.show()
        self.ui.x2Label.show()
        
        self.ui.x1SpinBox.show()
        self.ui.y1SpinBox.show()
        self.ui.x2SpinBox.show()
    
    def prepare_circles_mode(self):
        selected_mode = self.ui.LineManagerComboBox.currentText()
        
        if selected_mode == "Circle":
            self.ui.x1Label.setText(self.LABLE_FONT.format(name="X"))
            self.ui.y1Label.setText(self.LABLE_FONT.format(name="Y"))
            self.ui.x2Label.setText(self.LABLE_FONT.format(name="R"))
            
            self.ui.y2Label.hide()
            self.ui.y2SpinBox.hide()
        
            self.ui.x1Label.show()
            self.ui.y1Label.show()
            self.ui.x2Label.show()
            
            self.ui.x1SpinBox.show()
            self.ui.y1SpinBox.show()
            self.ui.x2SpinBox.show()
        elif selected_mode in ("Ellipse", "Hyperball"):
            self.ui.x1Label.setText(self.LABLE_FONT.format(name="X"))
            self.ui.y1Label.setText(self.LABLE_FONT.format(name="Y"))
            self.ui.x2Label.setText(self.LABLE_FONT.format(name="A"))
            self.ui.y2Label.setText(self.LABLE_FONT.format(name="B"))
        
            self.ui.x1Label.show()
            self.ui.y1Label.show()
            self.ui.x2Label.show()
            self.ui.y2Label.show()
            
            self.ui.x1SpinBox.show()
            self.ui.y1SpinBox.show()
            self.ui.x2SpinBox.show()
            self.ui.y2SpinBox.show()
        elif selected_mode == "Paraball":
            self.ui.x1Label.setText(self.LABLE_FONT.format(name="A"))
            self.ui.y1Label.setText(self.LABLE_FONT.format(name="H"))
            self.ui.x2Label.setText(self.LABLE_FONT.format(name="K"))
            
            self.ui.y2Label.hide()
            self.ui.y2SpinBox.hide()
        
            self.ui.x1Label.show()
            self.ui.y1Label.show()
            self.ui.x2Label.show()
            
            self.ui.x1SpinBox.show()
            self.ui.y1SpinBox.show()
            self.ui.x2SpinBox.show()
        else:
            print("Line mode selected!")
    
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

        color = QColor(255, 0, 0)  # Создаем объект QColor с RGB-значениями
        if self.draw_line_switcher:
            paint_template = self.grid.PAINT_TEMPLATES[self.ui.LineManagerComboBox.currentText()]
            self.paint_model = paint_template(coords=self.points)
            draw_points = self.paint_model.coords

            # pen = QPen(Qt.red)
            # pen.setWidth(2)
            # painter.setPen(pen)

            for i in range(len(draw_points)):
                point1 = self._calc_point(draw_points[i])
                # point2 = self._calc_point(draw_points[i + 1])
                self.cache_points.append((point1[0], point1[1]))
                if s := self.paint_model._c:
                    saturation = int(s[i] * 255)  # Преобразуем насыщенность в диапазон от 0 до 255
                    self.cache_saturation.append(saturation)
                    color.setHsv(color.hue(), saturation, color.value())  # Устанавливаем насыщенность цвета

                painter.setBrush(color)                        
                painter.drawRect(point1[0], point1[1], self.grid.spacing, self.grid.spacing)
        else:
            si = 0
            for x, y in self.cache_points:
                if self.cache_saturation:
                    saturation = self.cache_saturation[si]  # Преобразуем насыщенность в диапазон от 0 до 255
                    color.setHsv(color.hue(), saturation, color.value())  # Устанавливаем насыщенность цвета 
                    si += 1
                painter.setBrush(color)
                painter.drawRect(x, y, self.grid.spacing, self.grid.spacing)
        self.draw_line_switcher = False
        

    def draw_line(self):
        self.draw_line_switcher = True
        self.cache_points = []
        self.cache_saturation = []
        self.update()
        print("Line drawed!")

    def get_explain_data(self):
        if self.paint_model:
            return self.paint_model.res_table, str(self.paint_model)
        
        return {}, ''
    
    @property
    def points(self):
        return (
            self.ui.x1SpinBox.value(),
            self.ui.y1SpinBox.value(), 
            self.ui.x2SpinBox.value(),
            self.ui.y2SpinBox.value()
        )

    def _calc_point(self, coords):
        x1, y1 = coords
        return (
            x1 * self.grid.POINT_MULT + self.grid.start_x,
            self.grid.size -  y1 * self.grid.POINT_MULT + self.grid.start_y - 10
        )
        # return QPoint(
        #     x1 * self.grid.POINT_MULT,
        #     self.grid.size -  y1 * self.grid.POINT_MULT
        # ) + QPoint(self.grid.start_x, self.grid.start_y)