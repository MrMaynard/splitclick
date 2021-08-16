import time

# Used to write to a state channel
class PutChannel:
    def __init__(self, state, index, f, args=[]):
        self.state = state
        self.index = index
        self.f = f
        self.args = args

    def run(self):
        self.state._channel[self.index] = self.f(*self.args)
        self.state._channel_ready[self.index] = True

# Used to maintain async state
class State:

    RUNNING = "running"

    def intialize_channel(self, size):
        self._channel = [None for x in range(size)]
        self._channel_ready = [False for x in range(size)]

    def close_channel(self):
        self._channel = []
        self._channel_ready = []

    def get_channel(self, index):
        while not self._channel_ready[index]:
            time.sleep(0.01)
        return self._channel[index]

    def put_channel(self, index, f, args=None):
        return PutChannel(self, index, f, args)

    def __init__(self):
        self._state = dict()
        self._channel = []
        self._channel_ready = []

    def get(self, mutex):
        return self._state[mutex]

    def lock(self, mutex):
        if mutex in self._state:
            while self._state[mutex]:
                time.sleep(0.01)
        self._state[mutex] = True

    def unlock(self, mutex):
        self._state[mutex] = False