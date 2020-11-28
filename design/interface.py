import sys
import pygame
from PyQt5 import uic
from pyautogui import alert
from random import randint
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QLabel, QFileDialog
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

        if sys.platform == 'darwin':
            self.setFixedSize(1152, 452)
        else:
            self.setFixedSize(1152, 472)

        pygame.init()

        # constants
        ILLUMINATION_TIME = 300
        LETTER_TIME = 10
        MUSIC_TIME = 700

        self.NUMBER_OF_LETTERS = 25

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
        self.actionClose.triggered.connect(qApp.quit)

        self.actionInstruction_2.triggered.connect(self.open_help)

        self.actionEasy.triggered.connect(lambda: self.change_difficult('easy'))
        self.actionMedium.triggered.connect(lambda: self.change_difficult('medium'))
        self.actionHard.triggered.connect(lambda: self.change_difficult('hard'))

        # illumination
        self.illumination_timer = QTimer(self)
        self.illumination_timer.setInterval(ILLUMINATION_TIME)

        self.illumination = Illumination(self.illumination_timer)

        self.last_key = 0

        # ticker
        self.ticker_time = 1500

        self.ticker_timer = QTimer(self)
        self.ticker_timer.setInterval(self.ticker_time)
        self.ticker_timer.timeout.connect(self.create_letter)
        self.letters = list()

        self.letter_timer = QTimer(self)
        self.letter_timer.setInterval(LETTER_TIME)
        self.letter_timer.timeout.connect(self.move_all_letters)

        self.pushButton.clicked.connect(self.launch_ticker)

        self.pushButton_2.clicked.connect(self.restart)

        # result of the game
        self.result = QLabel(self)
        self.result.resize(1200, 100)
        self.result.move(885, 15)
        self.result.hide()
        self.result.setFont(QFont('Arial', 15))

        self.score = 0

        # music
        self.timer_music = QTimer(self)
        self.timer_music.setInterval(MUSIC_TIME)
        self.file = ''

    def keyPressEvent(self, event):
        if event.key() in self.QT_KEYS:
            if self.illumination_timer.isActive():
                self.PIANO_KEYS[self.last_key].setStyleSheet('background: none')

            if self.check_valid(self.QT_KEYS.index(event.key())):
                self.score += 1

                self.timer_music.start()
                self.timer_music.timeout.connect(lambda: stop_timer_music(self.timer_music))

                key_index = self.QT_KEYS.index(event.key())
                self.last_key = key_index

                self.illumination_timer.start()
                self.illumination_timer.timeout.connect(
                    lambda: self.illumination.stop_highlight_key(self.PIANO_KEYS[key_index]))
                self.illumination.highlight_key(self.PIANO_KEYS[key_index])

                play_song(str(key_index + 1) + '.wav')
            else:
                play_song('wrong.wav')

    @staticmethod
    def open_help():
        alert("""Привет! 

    Сейчас мы расскажем тебе несколько вещей, которые ты должен знать: в центре находится игровая линия, справа две кнопки. 
    Левая начинает игру, правая преждевременно останавливает. 
    Когда игра начнётся, буквы будут двигаться направо внутри большой чёрной линии. 
    Если буква достигнет красной черты, ты должен нажать указанную букву, тогда засчитается очко. 
    Всего нужно преодолеть 25 букв. 

    Удачи!""")

    def change_difficult(self, diff):
        if diff == 'easy':
            self.ticker_time = 2000
        if diff == 'medium':
            self.ticker_time = 1500
        if diff == 'hard':
            self.ticker_time = 1200
        self.ticker_timer.setInterval(self.ticker_time)

    def show_label_text(self):
        self.db = PointAnalysis()
        self.db.open()
        self.db.recording_score(self.score)
        self.max_score = self.db.max_score()
        self.average = round(self.db.averages_score())
        self.db.close()
        return f'Now score: {self.score}\nBest score: {self.max_score}\nAverage score: {self.average}'

    def check_valid(self, key_index):
        if self.letters:
            self.right_letter_text = self.letters[0].text()
            self.press_key = chr(self.QT_KEYS[key_index])
            for i in self.letters:
                if i.y() != 165:
                    return self.check_position(620, 700, i)
                else:
                    return self.check_position(220, 260, i)

    def check_position(self, x1, x2, letter):
        if x1 < letter.x() < x2 and self.press_key == self.right_letter_text:
            return True
        return False

    def stop_game(self):
        self.result.setText(self.show_label_text())
        self.result.show()
        self.score = 0

    def launch_ticker(self):
        if not (self.ticker_timer.isActive() and self.letter_timer.isActive()):
            self.result.hide()
            self.ticker = Ticker(create_random_list(self.NUMBER_OF_LETTERS))
            self.ticker_timer.start()
            self.letter_timer.start()
            self.letters = list()
            if self.file:
                play_song(self.file)

    def restart(self):
        self.ticker_timer.stop()
        self.letter_timer.stop()
        self.score = 0
        for i in self.letters:
            i.hide()

    def create_letter(self):
        if self.ticker.counter < self.NUMBER_OF_LETTERS:
            letter = QLabel(self.ticker.active_letter, self)
            letter.resize(100, 100)
            if randint(0, 1):
                letter.move(120, 35)
            else:
                letter.move(795, 165)
            letter.show()
            letter.setFont(QFont('Arial', 35))
            self.letters.append(letter)
            self.ticker.counter += 1
        else:
            self.ticker_timer.stop()

    def move_all_letters(self):
        for i in self.letters:
            if (i.x() > 780 and i.y() == 35) or (i.x() < 130 and i.y() == 165):
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
