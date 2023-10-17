import sys

from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtCore import Qt, QPoint

from view import MainView


class App(QApplication):
    current_view = None
    
    def __init__(self, *args):
        super().__init__(list(args))
        self.widgets = QStackedWidget()
        self.main_view = MainView()

        self._init_view()
        self._init_app()

    def _init_app(self):
        # add widgets
        self.widgets.addWidget(self.main_view)
        # set size
        self.widgets.setFixedWidth(700)
        self.widgets.setFixedHeight(700)
        # show
        self._switch_view(self.main_view)
        self.widgets.show()
    
    def _init_view(self):
        pass

    def _switch_view(self, view):
        self.current_view = view
        self.widgets.setCurrentWidget(self.current_view)


def application():
    app = App(sys.argv)
    app.setApplicationName("Line Drawer")
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
