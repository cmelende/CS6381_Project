from datetime import datetime
from uuid import uuid4
import matplotlib.pyplot as plt
from time import time
from zmqmw.middleware.handler.MessageHandler import MessageHandler


class PerfMessageHandler(MessageHandler):
    def __init__(self, log_name):
        self._messages = []
        self._name = log_name

    def handle_message(self, value: str) -> None:
        ts = float(value.split(":")[1])
        now = time() - ts
        self._messages.append(now)

    def flush(self):
        with open(f"{self._name}.csv", "a+") as file:
            file.writelines("\n".join(f"{i},{v}" for i, v in enumerate(self._messages)))
        plt.plot(range(len(self._messages)), self._messages)
        plt.savefig(f"{self._name}.png")
