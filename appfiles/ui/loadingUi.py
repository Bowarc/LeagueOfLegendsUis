from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QShortcut
from PyQt5.QtGui import QKeySequence, QPixmap, QFont
from PyQt5.QtCore import Qt

import appfiles.utils.assets as assets

WINDOW_SIZE = (1280, 720)


class loadingWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.assetsLoader = assets.assetsLoader()

        self.initUi()
        self.setupUi()
        self.applyQss("loading.qss")

        self.load_debug_action()

    def initUi(self):
        self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])

        self.setWindowFlags(
            Qt.Widget | QtCore.Qt.FramelessWindowHint)

        self.clicked = False
        QtGui.QFontDatabase.addApplicationFont(
            self.assetsLoader.getFont("Beaufort-Regular.ttf"))

    def setupUi(self):
        self.setObjectName("Window")

        logo_size = (501, 199)
        logo_pos = (self.get_size()[0]/2-logo_size[0]/2,
                    self.get_size()[1]/2-logo_size[1]/2 - 70)

        self.logoLabel = QtWidgets.QLabel(self)
        self.logoLabel.setGeometry(QtCore.QRect(
            logo_pos[0], logo_pos[1], logo_size[0], logo_size[1]))
        self.logoLabel.setPixmap(QtGui.QPixmap(
            QPixmap(self.assetsLoader.getImage("LeagueOfLinux.png"))))
        self.logoLabel.setObjectName("logo")

        loading_size = (100, 50)
        loading_pos = (self.get_size()[0]/2 - loading_size[0] / 2,
                       self.get_size()[1]/2 - loading_size[1] / 2 + 100)
        self.loadingLabel = QtWidgets.QLabel("Loading", self)
        self.loadingLabel.setGeometry(QtCore.QRect(
            loading_pos[0], loading_pos[1], loading_size[0], loading_size[1]))
        self.loadingLabel.setObjectName("loadingText")

        self.loadingBar = QtWidgets.QProgressBar(self)
        self.loadingBar.setGeometry(QtCore.QRect(550, 480, 211, 23))
        self.loadingBar.setValue(24)
        self.loadingBar.setObjectName("loadingBar")

    def get_size(self):
        return (self.frameGeometry().width(), self.frameGeometry().height())

    def load_debug_action(self):
        self.quitSc = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.quitSc.activated.connect(self.close)
        self.quitSc2 = QShortcut(QKeySequence('Escape'), self)
        self.quitSc2.activated.connect(self.close)

    def applyQss(self, fileName):
        path = self.assetsLoader.getQss(fileName)
        with open(path, "r") as f:
            self.setStyleSheet(f.read())

    def mousePressEvent(self, event):
        self.clicked = True
        self.old_pos = event.screenPos()

    def mouseReleaseEvent(self, event):
        self.clicked = False

    def mouseMoveEvent(self, qevent):

        if self.clicked:
            dx = self.old_pos.x() - qevent.screenPos().x()
            dy = self.old_pos.y() - qevent.screenPos().y()
            self.move(self.pos().x() - dx, self.pos().y() - dy)

        self.old_pos = qevent.screenPos()
        return QWidget.mouseMoveEvent(self, qevent)
