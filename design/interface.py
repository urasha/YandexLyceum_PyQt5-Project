import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from design.key_illumination import Illumination


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)

        self.actionClose_application_Ctrl_L.triggered.connect(qApp.quit)

        self.timer = QTimer(self)
        self.timer.setInterval(300)

        self.illumination = Illumination(self.timer)

        self.timer.timeout.connect(lambda: self.illumination.stop_highlight_key(self.label_2))  # тест на label_2

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:  # key_1 для теста
            self.timer.start()
            self.illumination.highlight_key(self.label_2)  # тест на label_2


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = MainForm()
    main_form.show()
    sys.exit(app.exec())
