import argparse
import signal
import sys

from PySide6.QtWidgets import QApplication
from lightbull import Lightbull, LightbullError

from .window import LightbullSimulatorMain
from .utils import fail


def run():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str, required=True, help="URL of the server")
    parser.add_argument("-p", "--password", type=str, required=True, help="Password for API")
    parser.add_argument("-r", "--reload", type=int, default=5, help="Number of reloads per second (default: 5)")
    args = parser.parse_args()

    # make ctrl-c work
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # connect to lightbull api
    try:
        api = Lightbull(args.url, args.password)
    except (LightbullError, OSError) as e:
        fail("Cannot connect to lightbull API: {}".format(e))

    # start ui
    app = QApplication([])
    main = LightbullSimulatorMain(api, args.reload)
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
