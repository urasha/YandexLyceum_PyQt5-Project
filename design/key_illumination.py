class Illumination:
    def __init__(self, timer):
        self.timer = timer

    @staticmethod
    def highlight_key(key):
        key.setStyleSheet('background: rgba(255, 20, 0, 0.5)')

    def stop_highlight_key(self, key):
        self.timer.stop()
        key.setStyleSheet('background: none')
