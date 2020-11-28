class Ticker:
    def __init__(self, letters):
        self.letters = letters
        self.counter = 0
        self.active_letter = self.letters[self.counter]

    def move_letter(self, letter):
        if self.counter < len(self.letters):
            self.active_letter = self.letters[self.counter]
        letter.move(letter.x() + 2 if letter.y() == 35 else letter.x() - 2, letter.y())
