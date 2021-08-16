import pynput
import time

class KeyHook:

    def __init__(self, key, mutex):
        self.key = "'" + key + "'"
        self.mutex = mutex

    def listen(self, state):
        def on_press(key):
            if str(key) == self.key:
                if state.get(self.mutex):
                    state.unlock(self.mutex)
                else:
                    state.lock(self.mutex)

        with pynput.keyboard.Listener(on_press=on_press) as kb_listener:
            kb_listener.join()