class Ticker:
    def __init__(self, letters):
        self.letters = letters
        self.counter = 0
        self.active_letter = self.letters[self.counter]

    def move_letter(self, letter):
        if self.counter < 50:
            self.active_letter = self.letters[self.counter]
        letter.move(letter.x() + 2.5, letter.y())
