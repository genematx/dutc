from functools import cached_property
from logging import getLogger, basicConfig, INFO
from sys import exit, argv

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QMenuBar, QMenu, QAction,
    QVBoxLayout, QGridLayout,
    QPushButton, QLabel, QDialog, QDialogButtonBox, QLineEdit,
)

logger = getLogger(__name__)
basicConfig(level=INFO)

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Simple Calculator'
        self.text = '1 / 3'
        self.precision = 2

        self.setWindowTitle = self.title
        self.setMenuBar(self.menu_bar)
        self.setCentralWidget(self.central_widget)

    def update(self):
        logger.info('update: self.text = %r; self.precision = %d', self.text, self.precision)
        editor = self.widgets['editor']
        result = self.widgets['result']
        result.setText(self.evaluate(editor.text(), precision=self.precision))

    @cached_property
    def central_widget(self):
        central_widget = QWidget()
        central_widget.setLayout(layout := QGridLayout())
        for (row, col), widg in self.grid.items():
            layout.addWidget(widg, row, col)
        return central_widget

    @cached_property
    def widgets(self):
        widgets = {
            'editor': QLineEdit(self.text),
            'result': QLabel(self.evaluate(self.text, precision=self.precision)),
        }
        @widgets['editor'].textChanged.connect
        def callback(text):
            self.text = text
            self.update()
        return widgets

    @cached_property
    def grid(self):
        widgets = self.widgets
        grid = {
            (0, 0): QLabel('Result'),     (0, 1): widgets['result'],
            (1, 0): QLabel('Expression'), (1, 1): widgets['editor'],
        }
        return grid

    @cached_property
    def menu_bar(self):
        menu_bar = QMenuBar()
        actions = {
            'quit':     QAction('&Quit',     self),
            'settings': QAction('&Settings', self),
        }
        menus = {
            'file':   (QMenu('&File', self), {actions['quit']}),
            'config': (QMenu('&Edit', self), {actions['settings']}),
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

        @actions['settings'].triggered.connect
        def callback():
            (diag := QDialog(window)).setLayout(layout := QVBoxLayout())
            widgets = {
                'label':  QLabel('Precision'),
                'editor': QLineEdit(f'{self.precision}'),
                'button': QPushButton('Done'),
            }
            for widg in widgets.values():
                layout.addWidget(widg)

            # TODO: YOUR CODE HERE
            ...
            widgets['button'].clicked.connect(diag.close)
            diag.exec_()
        return menu_bar

    @staticmethod
    def evaluate(text, *, precision):
        logger.info('evaluate: %r', text)
        try:
            return f'{eval(text):.{precision}f}'
        except Exception as e:
            return repr(e)

if __name__ == '__main__':
    app = QApplication(argv)
    window = CalculatorWindow()
    window.show()
    exit(app.exec())