import getopt
import sys
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from merged.examples.misc.app.options.AppOptions import AppOptions

TClient = TypeVar("TClient")


class App(ABC, Generic[TClient]):

    def __init__(self, app_options: AppOptions):
        self._app_options = app_options
        self._use_proxy = True
        try:
            opts, args = getopt.getopt(self._app_options.Argv,
                                       self._app_options.ShortOptions,
                                       self._app_options.LongOptions)
        except getopt.GetoptError:
            print("usage subscriber_one.py flags=")
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-f", "flag"):
                self._use_proxy = self.__use_proxy_client(arg)
            else:
                print(f'ignoring flag {opt}')

    @staticmethod
    def __use_proxy_client(flag_value: str):
        if flag_value == "proxy":
            return True
        elif flag_value == "notifier":
            return False
        else:
            print("invalid flag arg")
            sys.exit(2)

    @abstractmethod
    def run(self) -> TClient:
        pass
