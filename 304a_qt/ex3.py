from functools import cached_property
from logging import getLogger, basicConfig, INFO
from sys import exit, argv

from matplotlib import use
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from numpy import linspace
from sympy import lambdify
from sympy.parsing import parse_expr

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QMenuBar, QMenu, QAction,
    QVBoxLayout, QGridLayout,
    QPushButton, QLabel, QDialog, QDialogButtonBox, QLineEdit,
)

logger = getLogger(__name__)
basicConfig(level=INFO)

use('Qt5Agg')

class PlottingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Simple Plotter'

        self.setWindowTitle = self.title
        self.setMenuBar(self.menu_bar)
        self.setCentralWidget(self.central_widget)

    @cached_property
    def central_widget(self):
        central_widget = QWidget()
        central_widget.setLayout(layout := QGridLayout())
        for (row, col), widg in self.grid.items():
            layout.addWidget(widg, row, col)
        return central_widget

    @cached_property
    def widgets(self):
        default_expr = 'x**2 + 2*x + 1'
        default_lower_bound, default_upper_bound, default_samples = 0, 10, 100

        widgets = {
            'plot':       FigureCanvasQTAgg(fig := Figure(figsize=(10, 10), dpi=120)),
            'expression': QLineEdit(f'{default_expr}'),
            'lower':      QLineEdit(f'{default_lower_bound}'),
            'upper':      QLineEdit(f'{default_upper_bound}'),
            'samples':    QLineEdit(f'{default_samples}'),
        }
        widgets['plot'].axes = fig.add_subplot(111)

        # TODO: YOUR CODE HERE
        ...

        return widgets

    @cached_property
    def grid(self):
        widgets = self.widgets
        grid = {
            (0, 0): QLabel('Plot'),       (0, 1): widgets['plot'],
            (1, 0): QLabel('Expression'), (1, 1): widgets['expression'],
            (2, 0): QLabel('From'),       (2, 1): widgets['lower'],
            (3, 0): QLabel('To'),         (3, 1): widgets['upper'],
            (4, 0): QLabel('Samples'),    (4, 1): widgets['samples'],
        }
        return grid

    @cached_property
    def menu_bar(self):
        menu_bar = QMenuBar()
        actions = {
            'quit': QAction('&Quit',     self),
        }
        menus = {
            'file': (QMenu('&File', self), {actions['quit']}),
        }
        for menu, menu_actions in menus.values():
            for act in menu_actions:
                menu.addAction(act)
            menu_bar.addMenu(menu)

        @actions['quit'].triggered.connect
        def callback():
            (dialog := QDialog()).setLayout(layout := QVBoxLayout())
            layout.addWidget(button_box :=
                QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            )
            button_box.accepted.connect(app.quit)
            button_box.rejected.connect(dialog.close)
            dialog.exec_()

        return menu_bar

if __name__ == '__main__':
    app = QApplication(argv)
    window = PlottingWindow()
    window.show()
    exit(app.exec())