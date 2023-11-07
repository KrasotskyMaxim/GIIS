import sys

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication, 
    QStackedWidget,
    QAction, 
    QMenuBar,
)

from view import MainView, ExplainView


class LineDrawer(QMainWindow):
    current_view = None
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(700, 730)
        
        self.widgets = QStackedWidget()
        self.main_view = MainView()
        self.explain_view = ExplainView()
        
        self.widgets.addWidget(self.main_view)
        self.widgets.addWidget(self.explain_view)
        
        self._init_view()

        self.setMenuBar(self.menu_bar())

        self._goto_slines()
        self.setCentralWidget(self.widgets)
    
    def menu_bar(self):
        menu_bar = QMenuBar(self)
        options_menu = menu_bar.addMenu("Options")

        slines = QAction("SLines", self)
        slines.triggered.connect(self._goto_slines)
        options_menu.addAction(slines)

        circles = QAction("Circles", self)
        circles.triggered.connect(self._goto_circles)
        options_menu.addAction(circles)

        return menu_bar
    
    def _init_view(self):
        self.explain_view.ui.BackPushButton.clicked.connect(lambda: self._goto_slines(draw=True))
        
    def _switch_view(self, view):
        self.current_view = view
        self.widgets.setCurrentWidget(self.current_view)
    
    def _goto_explain(self):
        table_data, model_name = self.main_view.get_explain_data()
        if table_data:
            self.explain_view.set_table_data(
                data=table_data,
                model_name=model_name
            )
            self._switch_view(self.explain_view)
        else:
            print("line not drawed!")

    def _goto_slines(self, draw=False):
        if draw:
            self.main_view.draw_line()
        self.main_view.prepare_slines()
        self._switch_view(self.main_view)
        
    def _goto_circles(self, draw=False):
        if draw:
            ...
        self.main_view.prepare_circles()
        self._switch_view(self.main_view)

def application():
    app = QApplication(sys.argv)
    app.setApplicationName("Line Drawer")
    window = LineDrawer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
