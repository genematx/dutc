from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from sys import exit, argv

if __name__ == '__main__':
    app = QApplication(argv)

    window = QWidget()
    window.setWindowTitle('Simple Counter')

    layout = QVBoxLayout()
    window.setLayout(layout)

    count = 0

    label = QLabel()
    label.setText(f'Count: {count}')

    buttons = {
        'inc': QPushButton('Increment'),
        'dec': QPushButton('Decrement'),
        'quit': QPushButton('Quit')
    }

    buttons['inc'].clicked.connect(lambda: count + 1 ) # TODO: YOUR CODE HERE
    buttons['dec'].clicked.connect(lambda: count - 1 ) # TODO: YOUR CODE HERE
    buttons['quit'].clicked.connect(app.exit)

    layout.addWidget(label)
    for but in buttons.values():
        layout.addWidget(but)

    window.show()
    exit(app.exec())
