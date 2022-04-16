from PySide6 import QtWidgets, QtCore

from .led import LedWidget


class LightbullSimulatorMain(QtWidgets.QMainWindow):
    def __init__(self, api, reload_per_second):
        super(LightbullSimulatorMain, self).__init__()
        self._api = api
        self.initUI()
        self.initTimer(reload_per_second)

    def initUI(self):
        self.setWindowTitle("Lightbull Simulator")

        self._widget = LedWidget(self._api)
        self.setCentralWidget(self._widget)

    def initTimer(self, reload_per_second):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000.0/reload_per_second)
        self.timer.timeout.connect(self._widget.update)
        self.timer.start()
