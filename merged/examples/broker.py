import sys

from merged.examples.misc.app.App import App
from merged.examples.misc.app.BrokerApp import BrokerApp
from merged.examples.misc.app.options.AppOptions import AppOptions
from merged.examples.misc.logger.DateTimeConsoleLogger import DateTimeConsoleLogger
from merged.middleware.adapter.BrokerClient import BrokerClient

short_options = "f"
long_options = ["flag="]


def main(argv) -> None:
    options: AppOptions = AppOptions(argv, DateTimeConsoleLogger())
    app: App[BrokerClient] = BrokerApp(options)
    client = app.create_client()


if __name__ == "__main__":
    main(sys.argv[1:])
