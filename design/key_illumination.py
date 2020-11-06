class Illumination:
    def __init__(self, timer):
        self.timer = timer

    @staticmethod
    def highlight_key(key):
        key.setStyleSheet('background: rgba(200, 100, 0, 0.3)')

    def stop_highlight_key(self, key):
        self.timer.stop()
        key.setStyleSheet('background: none')
