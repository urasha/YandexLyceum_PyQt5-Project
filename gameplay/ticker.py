class Ticker:
    def __init__(self, letters):
        self.letters = letters
        self.counter = 0
        self.active_letter = self.letters[self.counter]

    @staticmethod
    def move_letter(letter):
        letter.move(letter.x() + 2, letter.y())

    def show_letter(self):
        pass
