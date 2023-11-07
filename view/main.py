from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QFont, QColor
from PyQt5.QtCore import Qt

from view.forms import MainForm, GridDataForm, DrawTypes


class MainView(QWidget):
    LABLE_FONT = "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">{name}</span></p></body></html>"
    DEBUG_MODE = {
        "enable": False,
        "started": False,
        "step": 0,
    }
    draw = False

    def __init__(self):
        super(MainView, self).__init__()
        self.ui = MainForm(self)
        self.grid = GridDataForm(self)
    
        self.paint_model = None
        self.debug_points = []
        self.debug_saturation = []
        
        self.init_UI()
        
    def init_UI(self):
        self.ui.DrawPushButton.clicked.connect(self.draw_figure)
        self.ui.DrawManagerComboBox.currentIndexChanged.connect(self.change_ring_mode)
        
        self.ui.DebugPushButton.clicked.connect(self._switch_debug)
        self.ui.ForwardDebugPushButton.clicked.connect(self._forward_debug)
        self.ui.BackDebugPushButton.clicked.connect(self._back_debug)
        
        self.ui.x1SpinBox.valueChanged.connect(self._changed_box)
        self.ui.x2SpinBox.valueChanged.connect(self._changed_box)
        self.ui.y1SpinBox.valueChanged.connect(self._changed_box)
        self.ui.y2SpinBox.valueChanged.connect(self._changed_box)
        self.ui.DrawManagerComboBox.currentIndexChanged.connect(self._changed_box)
        
        self._hide_interface()
                
    def _changed_box(self):
        if self.DEBUG_MODE["enable"]:
            self.clear_cache()
            self._calc_debug_points()

    def _forward_debug(self):
        if not self.DEBUG_MODE["enable"]:
            return
        
        if not self.DEBUG_MODE["started"]:
            self._calc_debug_points()
            self.DEBUG_MODE["started"] = True
        
        if self.DEBUG_MODE["step"] < len(self.debug_points):
            self.DEBUG_MODE["step"] += 1
        
        self.draw = True
        self.update()
            
    def _back_debug(self):
        if not self.DEBUG_MODE["enable"]:
            return
    
        if not self.DEBUG_MODE["started"]:
            self._calc_debug_points()
            self.DEBUG_MODE["started"] = True
        
        if self.DEBUG_MODE["step"] > 0:
            self.DEBUG_MODE["step"] -= 1
            
        self.draw = True
        self.update()
        
    def _calc_debug_points(self):
        saturation = 255
        paint_template = self.grid.PAINT_TEMPLATES[self.ui.DrawManagerComboBox.currentText()]
        self.paint_model = paint_template(values=self.points)
        draw_points = self.paint_model.points
        
        for i in range(len(draw_points)):
            point = self._calc_point(draw_points[i])
            
            if self._is_out_point(point[0], point[1]):
                continue
            
            if s := self.paint_model.saturation:
                saturation = int(s[i] * 255)

            self.debug_points.append((point[0], point[1]))
            self.debug_saturation.append(saturation)

    def _hide_interface(self):
        self.ui.ForwardDebugPushButton.hide()
        self.ui.BackDebugPushButton.hide()
    
    def _switch_debug(self):
        if not self.DEBUG_MODE["enable"]:
            self.clear_grid()
            self.DEBUG_MODE["enable"] = True
            
            self.ui.DebugPushButton.setText("DEBUG: ON")
            self.ui.DrawPushButton.hide()
            self.ui.ForwardDebugPushButton.show()
            self.ui.BackDebugPushButton.show()
        else:
            self._reset_debug_mode()
            self.clear_grid()
            
            self.ui.DebugPushButton.setText("DEBUG: OFF")
            self.ui.DrawPushButton.show()
            self.ui.ForwardDebugPushButton.hide()
            self.ui.BackDebugPushButton.hide()
    
    def _reset_debug_mode(self):
        self.DEBUG_MODE = {
            "enable": False,
            "started": False,
            "step": 0,
        }
    
    def prepare_sline(self):
        while (c := self.ui.DrawManagerComboBox.count()) != 3:
            if c < 3:
                self.ui.DrawManagerComboBox.addItem("")
            elif c > 3:    
                self.ui.DrawManagerComboBox.removeItem(0)

        self.ui.DrawManagerComboBox.setItemText(0, "CDA")
        self.ui.DrawManagerComboBox.setItemText(1, "Brazenhem")
        self.ui.DrawManagerComboBox.setItemText(2, "By")
        
        self.ui.DrawManagerComboBox.setCurrentIndex(0)
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
        
        self.ui.x1SpinBox.setMinimum(-self.grid.COORD_LEN // 2)
        self.ui.x1SpinBox.setMaximum(self.grid.COORD_LEN // 2)
        self.ui.x2SpinBox.setMinimum(-self.grid.COORD_LEN // 2)
        self.ui.x2SpinBox.setMaximum(self.grid.COORD_LEN // 2)
        self.ui.y1SpinBox.setMinimum(-self.grid.COORD_LEN // 2)
        self.ui.y1SpinBox.setMaximum(self.grid.COORD_LEN // 2)
        self.ui.y2SpinBox.setMinimum(-self.grid.COORD_LEN // 2)
        self.ui.y2SpinBox.setMaximum(self.grid.COORD_LEN // 2)
        
    def prepare_ring(self):
        while (c := self.ui.DrawManagerComboBox.count()) != 4:
            if c < 4:
                self.ui.DrawManagerComboBox.addItem("")
            elif c > 4:    
                self.ui.DrawManagerComboBox.removeItem(0)

        self.ui.DrawManagerComboBox.setItemText(0, "Circle")
        self.ui.DrawManagerComboBox.setItemText(1, "Ellipse")
        self.ui.DrawManagerComboBox.setItemText(2, "Hyperball")
        self.ui.DrawManagerComboBox.setItemText(3, "Paraball")
        
        # circle by default
        self.ui.DrawManagerComboBox.setCurrentIndex(0)
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
        
        self.ui.x1SpinBox.setMinimum(-self.grid.COORD_LEN // 2)
        self.ui.x1SpinBox.setMaximum(self.grid.COORD_LEN // 2)
        self.ui.y1SpinBox.setMinimum(-self.grid.COORD_LEN // 2)
        self.ui.y1SpinBox.setMaximum(self.grid.COORD_LEN // 2)
        self.ui.x2SpinBox.setMinimum(0)
        self.ui.x2SpinBox.setMaximum(self.grid.COORD_LEN // 2)
        self.ui.y2SpinBox.setMinimum(0)
        self.ui.y2SpinBox.setMaximum(self.grid.COORD_LEN // 2)
    
    def change_ring_mode(self):
        selected_mode = self.ui.DrawManagerComboBox.currentText()
        
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
            
            self.ui.x2SpinBox.setMinimum(0)
            self.ui.x2SpinBox.setMaximum(self.grid.COORD_LEN // 2)
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
            
            self.ui.x2SpinBox.setMinimum(0)
            self.ui.x2SpinBox.setMaximum(self.grid.COORD_LEN // 2)
            self.ui.y2SpinBox.setMinimum(0)
            self.ui.y2SpinBox.setMaximum(self.grid.COORD_LEN // 2)    
        elif selected_mode == "Paraball":
            self.ui.x1Label.setText(self.LABLE_FONT.format(name="X"))
            self.ui.y1Label.setText(self.LABLE_FONT.format(name="A"))
            self.ui.x2Label.setText(self.LABLE_FONT.format(name="B"))
            self.ui.y2Label.setText(self.LABLE_FONT.format(name="C"))
            
            self.ui.x1Label.show()
            self.ui.y1Label.show()
            self.ui.x2Label.show()
            self.ui.y2Label.show()
            
            self.ui.x1SpinBox.show()
            self.ui.y1SpinBox.show()
            self.ui.x2SpinBox.show()
            self.ui.y2SpinBox.show()
            
            self.ui.x1SpinBox.setMinimum(0)
            self.ui.x1SpinBox.setMaximum(self.grid.COORD_LEN // 2)  
            self.ui.x2SpinBox.setMinimum(-self.grid.COORD_LEN // 2)
            self.ui.x2SpinBox.setMaximum(self.grid.COORD_LEN // 2)
            self.ui.y1SpinBox.setMinimum(-self.grid.COORD_LEN // 2)
            self.ui.y1SpinBox.setMaximum(self.grid.COORD_LEN // 2)
            self.ui.y2SpinBox.setMinimum(-self.grid.COORD_LEN // 2)
            self.ui.y2SpinBox.setMaximum(self.grid.COORD_LEN // 2)    

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor(255, 0, 0)
        saturation = 255

        def _draw_grid():
            # Draw thick lines for quadrants
            thick_pen = QPen(Qt.black)
            thick_pen.setWidth(4)
            painter.setPen(thick_pen)
            half_x = self.grid.start_x + self.grid.size // 2
            half_y = self.grid.start_y + self.grid.size // 2
            painter.drawLine(half_x, self.grid.start_y, half_x, self.grid.start_y + self.grid.size)
            painter.drawLine(self.grid.start_x, half_y, self.grid.start_x + self.grid.size, half_y)
            
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
            # Label X on the right in the middle
            painter.drawText(self.grid.start_x + self.grid.size + 10, half_y + 5, "X")
            # Label Y at the top in the middle
            painter.drawText(half_x - 10, self.grid.start_y - 10, "Y")

        _draw_grid()
        
        if self.draw:            
            if self.DEBUG_MODE["enable"]:
                if self.DEBUG_MODE["started"]:
                    si = 0
                    for x, y in self.debug_points[:self.DEBUG_MODE["step"]]:
                        if self.debug_saturation:
                            saturation = self.debug_saturation[si]  # Преобразуем насыщенность в диапазон от 0 до 255
                            color.setHsv(color.hue(), saturation, color.value())  # Устанавливаем насыщенность цвета 
                            si += 1
                        painter.setBrush(color)
                        painter.drawRect(x, y, self.grid.spacing, self.grid.spacing)        
            else:
                paint_template = self.grid.PAINT_TEMPLATES[self.ui.DrawManagerComboBox.currentText()]
                self.paint_model = paint_template(values=self.points)
                draw_points = self.paint_model.points
                
                for i in range(len(draw_points)):
                    point = self._calc_point(draw_points[i])
                    
                    if self._is_out_point(point[0], point[1]):
                        continue
                    
                    if s := self.paint_model.saturation:
                        saturation = int(s[i] * 255)

                    color.setHsv(color.hue(), saturation, color.value())
                    painter.setBrush(color)               
                    painter.drawRect(point[0], point[1], self.grid.spacing, self.grid.spacing)
        self.draw = False
        
    def _is_out_point(self, x , y):
        return x not in range(self.grid.start_x - 1, self.grid.end_x + 1) or y not in range(self.grid.start_y - 1, self.grid.end_y - 1) 

    def draw_figure(self):
        self.draw = True
        self.update()
    
    def clear_grid(self):
        self.draw = False
        self.debug_points = []
        self.debug_saturation = []
        self.update()
    
    def clear_cache(self):
        self.DEBUG_MODE["step"] = 0
        self.debug_points = []
        self.debug_saturation = []

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
            x1 * self.grid.spacing + self.grid.start_x + self.grid.size // 2,
            self.grid.size // 2 - (y1 + 1) * self.grid.spacing + self.grid.start_y
        )
