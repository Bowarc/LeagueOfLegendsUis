from PyQt5.QtCore import QRect, QRectF, QSize, Qt, QTimer
from PyQt5.QtGui import QColor, QPainter, QPalette, QPen
from PyQt5.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
                             QSizePolicy, QWidget)


class CircleWidget(QWidget):
    def __init__(self, parent=None):
        super(CircleWidget, self).__init__(parent)

        self.floatBased = False
        self.antialiased = False
        self.frameNo = 0

        self.setBackgroundRole(QPalette.Base)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setFloatBased(self, floatBased):
        self.floatBased = floatBased
        self.update()

    def setAntialiased(self, antialiased):
        self.antialiased = antialiased
        self.update()

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(180, 180)

    def nextAnimationFrame(self):
        self.frameNo += 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, self.antialiased)
        painter.translate(self.width() / 2, self.height() / 2)

        for diameter in range(0, 256, 9):
            delta = abs((self.frameNo % 128) - diameter / 2)
            alpha = 255 - (delta * delta) / 4 - diameter
            if alpha > 0:
                painter.setPen(QPen(QColor(0, diameter / 2, 127, alpha), 3))

                if self.floatBased:
                    painter.drawEllipse(QRectF(-diameter / 2.0,
                                               -diameter / 2.0, diameter, diameter))
                else:
                    painter.drawEllipse(QRect(-diameter / 2,
                                              -diameter / 2, diameter, diameter))


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        aliasedLabel = self.createLabel("Aliased")
        antialiasedLabel = self.createLabel("Antialiased")
        intLabel = self.createLabel("Int")
        floatLabel = self.createLabel("Float")

        layout = QGridLayout()
        layout.addWidget(aliasedLabel, 0, 1)
        layout.addWidget(antialiasedLabel, 0, 2)
        layout.addWidget(intLabel, 1, 0)
        layout.addWidget(floatLabel, 2, 0)

        timer = QTimer(self)

        for i in range(2):
            for j in range(2):
                w = CircleWidget()
                w.setAntialiased(j != 0)
                w.setFloatBased(i != 0)

                timer.timeout.connect(w.nextAnimationFrame)

                layout.addWidget(w, i + 1, j + 1)

        timer.start(100)
        self.setLayout(layout)

        self.setWindowTitle("Concentric Circles")

    def createLabel(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setMargin(2)
        label.setFrameStyle(QFrame.Box | QFrame.Sunken)
        return label


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
