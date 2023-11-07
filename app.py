import sys

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication, 
    QAction, 
    QMenuBar,
)

from view import MainView
from view.forms import DrawTypes


class LineDrawer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(700, 730)
        self.view = MainView()
        
        self.setMenuBar(self._menu_bar())

        self._goto_sline()
        self.setCentralWidget(self.view)
    
    def _menu_bar(self):
        menu_bar = QMenuBar(self)
        options_menu = menu_bar.addMenu("Options")

        sline = QAction(DrawTypes.SLINE, self)
        sline.triggered.connect(self._goto_sline)
        options_menu.addAction(sline)

        ring = QAction(DrawTypes.RING, self)
        ring.triggered.connect(self._goto_ring)
        options_menu.addAction(ring)

        return menu_bar

    def _goto_sline(self):
        self.view.clear_grid()
        self.view.prepare_sline()

    def _goto_ring(self, draw=False):
        self.view.clear_grid()
        self.view.prepare_ring()


def application():
    app = QApplication(sys.argv)
    app.setApplicationName("Line Drawer")
    window = LineDrawer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
