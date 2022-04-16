from PySide6 import QtWidgets, QtGui
from lightbull import LightbullError
from .utils import fail


class LedWidget(QtWidgets.QWidget):
    """ Main widgets containing all parts. """
    def __init__(self, api):
        super(LedWidget, self).__init__()
        self._api = api
        self.initUI()

    def initUI(self):
        try:
            parts = self._api.config().get("parts", None)
            data = self._api.simulator()
        except LightbullError as e:
            fail("Cannot query lightbull API: {}".format(e))

        if not parts:
            fail("No parts defined in lightbull")

        self._parts = {}
        hbox = QtWidgets.QVBoxLayout()
        for part in parts:
            partwidget = LedPartWidget(part, len(data[part]))
            hbox.addWidget(partwidget)
            self._parts[part] = partwidget
        self.setLayout(hbox)

    def update(self):
        try:
            data = self._api.simulator()

            for part, partdata in data.items():
                self._parts[part].update(partdata)
        except (LightbullError, OSError) as e:
            print("Cannot query lightbull API: {}".format(e))


class LedPartWidget(QtWidgets.QWidget):
    def __init__(self, partname, numleds):
        """ Widget for one part, containing name and LED pixels. """
        super(LedPartWidget, self).__init__()

        self.title = QtWidgets.QLabel(partname)

        self._graphicscene = QtWidgets.QGraphicsScene()
        self._graphicwidget = QtWidgets.QGraphicsView(self._graphicscene)
        self._graphicwidget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self._leds = []
        for i in range(numleds):
            led = GraphicsLed(i)
            led.setColor(0, 0, 0)
            self._graphicscene.addItem(led)
            self._leds.append(led)

        hbox = QtWidgets.QVBoxLayout()
        hbox.addWidget(self.title)
        hbox.addWidget(self._graphicwidget)
        self.setLayout(hbox)

    def update(self, data):
        for i, led in enumerate(self._leds):
            led.setColor(data[i]["r"], data[i]["g"], data[i]["b"])


class GraphicsLed(QtWidgets.QGraphicsRectItem):
    """ Widget to render the LED pixels of one part. """
    def __init__(self, counter=0):
        super(GraphicsLed, self).__init__(counter * 10, 0, 10, 10)
        self.setColor(0, 0, 0)

    def setColor(self, r, g, b):
        brush = QtGui.QBrush(QtGui.QColor(r, g, b))
        pen = QtGui.QPen(brush, 0)
        self.setBrush(brush)
        self.setPen(pen)
