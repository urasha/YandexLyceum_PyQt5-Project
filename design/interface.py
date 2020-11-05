import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic


class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('model.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = MainForm()
    main_form.show()
    sys.exit(app.exec())
