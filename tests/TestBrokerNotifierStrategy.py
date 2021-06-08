import asyncio
import threading
import unittest
from time import sleep
from unittest.mock import Mock

from zmqmw.implementations.notifier.broker.BrokerNotifierStrategy import BrokerNotifierStrategy
from zmqmw.middleware.strategy.BrokerStrategy import BrokerStrategy


class TestBrokerNotifierStrategy(unittest.TestCase):

    def test_run_does_not_throw_error(self):
        logger_mock = Mock()
        broker_notifier_strategy = BrokerNotifierStrategy("127.0.0.1", "5500", logger_mock)
        try:
            asyncio.create_task(self.__run_broker_notifier_strategy(broker_notifier_strategy))

            # let it run for a moment to make sure that we dont run into any errors
            sleep(5)
            self.__stop_broker_notifier_strategy(broker_notifier_strategy)

        except Exception as e:
            self.fail("something went wrong with starting or stopping the broker")

    @staticmethod
    def __stop_broker_notifier_strategy(strat: BrokerStrategy):
        strat.close()

    @staticmethod
    async def __run_broker_notifier_strategy(strat: BrokerStrategy):
        strat.run()


if __name__ == '__main__':
    unittest.main()


class thread_with_exception(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):

        # target function of the thread class
        try:
            while True:
                print('running ' + self.name)
        finally:
            print('ended')

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')