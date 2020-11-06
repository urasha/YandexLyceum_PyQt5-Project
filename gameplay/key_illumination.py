def highlight_key(key):
    key.setStyleSheet('background: rgba(200, 100, 0, 0.3)')


def stop_highlight(timer, key):
    timer.stop()
    key.setStyleSheet('background: none')