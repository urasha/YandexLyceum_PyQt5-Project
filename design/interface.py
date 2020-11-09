import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from design.key_illumination import Illumination
import pygame
from design.music_playback import play_song


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        pygame.init()

        # constants
        ILLUMINATION_TIME = 300

        self.PIANO_KEYS = [self.label_2, self.label_3, self.label_4,
                           self.label_5, self.label_6, self.label_7,
                           self.label_8, self.label_9, self.label_10,
                           self.label_11, self.label_12, self.label_13,
                           self.label_14, self.label_15, self.label_16,
                           self.label_17, self.label_18, self.label_19,
                           self.label_20, self.label_21, self.label_22,
                           self.label_23, self.label_24, self.label_25,
                           self.label_26, self.label_27]

        self.QT_KEYS = [Qt.Key_Q, Qt.Key_W, Qt.Key_E, Qt.Key_R,
                        Qt.Key_T, Qt.Key_Y, Qt.Key_U, Qt.Key_I, Qt.Key_O,
                        Qt.Key_P, Qt.Key_A, Qt.Key_S, Qt.Key_D, Qt.Key_F,
                        Qt.Key_G, Qt.Key_H, Qt.Key_J, Qt.Key_K,
                        Qt.Key_L, Qt.Key_Z, Qt.Key_X, Qt.Key_C, Qt.Key_V,
                        Qt.Key_B, Qt.Key_N, Qt.Key_M]

        # app actions
        self.actionClose_application_Ctrl_L.triggered.connect(qApp.quit)

        # timer for illumination
        self.timer = QTimer(self)
        self.timer.setInterval(ILLUMINATION_TIME)

        self.illumination = Illumination(self.timer)

        self.last_key = 0

    def keyPressEvent(self, event):
        if event.key() in self.QT_KEYS:
            if self.timer.isActive():
                self.PIANO_KEYS[self.last_key].setStyleSheet('background: none')

            self.timer.start()
            key_index = self.QT_KEYS.index(event.key())
            self.last_key = key_index
            self.timer.timeout.connect(lambda: self.illumination.stop_highlight_key(self.PIANO_KEYS[key_index]))
            self.illumination.highlight_key(self.PIANO_KEYS[key_index])

            play_song(str(key_index + 1) + '.wav')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = MainForm()
    main_form.show()
    sys.exit(app.exec())
