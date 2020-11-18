import sys
import pygame
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from design.key_illumination import Illumination
from design.music_playback import play_song, stop_timer_music
from gameplay.random_list import create_random_list
from gameplay.ticker import Ticker
from gameplay.point_analysis import PointAnalysis


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        pygame.init()

        # constants
        ILLUMINATION_TIME = 300
        TICKER_TIME = 1500
        LETTER_TIME = 10
        MUSUC_TIME = 700

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
        self.actionClose_Ctrl_L.triggered.connect(qApp.quit)

        # illumination
        self.illumination_timer = QTimer(self)
        self.illumination_timer.setInterval(ILLUMINATION_TIME)

        self.illumination = Illumination(self.illumination_timer)

        self.last_key = 0

        self.timer_music = QTimer(self)
        self.timer_music.setInterval(MUSUC_TIME)

        # ticker
        self.ticker_timer = QTimer(self)
        self.ticker_timer.setInterval(TICKER_TIME)
        self.ticker_timer.timeout.connect(self.create_letter)
        self.letters = list()

        self.letter_timer = QTimer(self)
        self.letter_timer.setInterval(LETTER_TIME)
        self.letter_timer.timeout.connect(self.move_all_letters)

        self.pushButton.clicked.connect(self.launch_ticker)

        self.pushButton_2.clicked.connect(self.restart)

        # result of the game
        self.result = QLabel(self)
        self.result.resize(750, 100)
        self.result.move(120, 15)
        self.result.hide()
        self.result.setFont(QFont('Arial', 25))

        self.score = 0

    def keyPressEvent(self, event):
        if event.key() in self.QT_KEYS:
            if self.illumination_timer.isActive():
                self.PIANO_KEYS[self.last_key].setStyleSheet('background: none')
            if self.timer_music.isActive():
                pass
            if self.check_valid(self.QT_KEYS.index(event.key())):
                self.score += 1
                print(self.score)
                self.illumination_timer.start()
                key_index = self.QT_KEYS.index(event.key())
                self.last_key = key_index
                self.timer_music.start()
                self.illumination_timer.timeout.connect(
                    lambda: self.illumination.stop_highlight_key(self.PIANO_KEYS[key_index]))
                self.timer_music.timeout.connect(lambda: stop_timer_music(self.timer_music))
                self.illumination.highlight_key(self.PIANO_KEYS[key_index])
                play_song(str(key_index + 1) + '.wav')
            else:
                play_song('wrong.wav')

    def show_label_text(self):
        self.db = PointAnalysis()
        self.db.open()
        self.db.recording_score(self.score)
        self.max_score = self.db.max_score()
        self.average = round(self.db.averages_score())
        self.db.close()
        return f'Game score: {self.score} | Max score: {self.max_score} | Average score: {self.average}'

    def check_valid(self, key_index):
        if self.letters:
            right_letter_text = self.letters[0].text()
            press_key = chr(self.QT_KEYS[key_index])
            for i in self.letters:
                if 620 < i.x() < 700 and press_key == right_letter_text:
                    return True
                else:
                    return False

    def stop_game(self):
        self.result.setText(self.show_label_text())
        self.result.show()
        self.score = 0

    def launch_ticker(self):
        if not (self.ticker_timer.isActive() and self.letter_timer.isActive()):
            self.result.hide()
            self.ticker = Ticker(create_random_list())
            self.ticker_timer.start()
            self.letter_timer.start()
            self.letters = list()

    def restart(self):
        self.ticker_timer.stop()
        self.letter_timer.stop()
        self.score = 0
        for i in self.letters:
            i.hide()

    def create_letter(self):
        if self.ticker.counter < 25:
            letter = QLabel(self.ticker.active_letter, self)
            letter.resize(100, 100)
            letter.move(120, 95)
            letter.show()
            letter.setFont(QFont('Arial', 35))
            self.letters.append(letter)
            self.ticker.counter += 1

        else:
            self.ticker_timer.stop()

    def move_all_letters(self):
        if self.letters:
            for i in self.letters:
                if i.x() > 780:
                    if len(self.letters) == 1:
                        self.stop_game()
                    i.hide()
                    self.letters.remove(i)
                self.ticker.move_letter(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = MainForm()
    main_form.show()
    sys.exit(app.exec())
