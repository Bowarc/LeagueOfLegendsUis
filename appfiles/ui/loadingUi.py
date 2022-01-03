from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QShortcut
from PyQt5.QtGui import QKeySequence, QPixmap, QFont, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer

import math

import time

import appfiles.utils.physics as physics

import appfiles.utils.assets as assets

WINDOW_SIZE = (1280, 720)


class loadingWindow(QWidget):
    def __init__(self, logger):
        QWidget.__init__(self)

        self.logger = logger

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
        QtGui.QFontDatabase.addApplicationFont(
            self.assetsLoader.getFont("Beaufort-Bold.ttf"))

        # init the rotating lines
        self.animation_angle = 0
        self.animation_line_size = 10
        self.animation_line_distaance_from_center = 320
        self.animation_line_color = "#252929"
        self.animation_rotating_speed = 10  # degree per seccond
        self.animation_last_angle_update = time.time()

        self.animation_painterUpdateTimer = QTimer(self)
        self.animation_painterUpdateTimer.timeout.connect(self.update)
        self.animation_painterUpdateTimer.start(0)

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

        loading_size = (110, 30)
        loading_pos = (self.get_size()[0]/2 - loading_size[0] / 2,
                       self.get_size()[1]/2 - loading_size[1] / 2 + 70)
        self.loadingLabel = QtWidgets.QLabel("LOADING", self)
        self.loadingLabel.setGeometry(QtCore.QRect(
            loading_pos[0], loading_pos[1], loading_size[0], loading_size[1]))
        self.loadingLabel.setObjectName("loadingText")

        loadingBar_size = (
            200, 11
        )
        loadingBar_pos = (
            self.get_size()[0]/2 - loadingBar_size[0]/2,
            self.get_size()[1]/2 - loadingBar_size[1]/2 + 100,
        )
        self.loadingBar = QtWidgets.QProgressBar(self)
        self.loadingBar.setGeometry(QtCore.QRect(
            loadingBar_pos[0], loadingBar_pos[1], loadingBar_size[0], loadingBar_size[1]))
        self.loadingBar.setValue(75)
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

    def mouseMoveEvent(self, event):

        if self.clicked:
            dx = self.old_pos.x() - event.screenPos().x()
            dy = self.old_pos.y() - event.screenPos().y()
            self.move(self.pos().x() - dx, self.pos().y() - dy)

        self.old_pos = event.screenPos()
        return QWidget.mouseMoveEvent(self, event)

    def paintEvent(self, event):
        self.update_painter_angle()
        painter = QPainter(self)
        pen = QPen(QColor(self.animation_line_color), 1, Qt.SolidLine)
        painter.setPen(pen)

        # center of the window
        origin = (self.get_size()[0]/2, self.get_size()[1]/2)

        ray_number = 200
        for i in range(ray_number):
            angle = self.animation_angle + i * (360 / ray_number)
            point1 = physics.rotate_point(origin, (
                self.get_size()[0]/2 +
                self.animation_line_distaance_from_center,
                self.get_size()[1]/2
            ), angle)

            point2 = physics.rotate_point(origin, (
                self.get_size()[0]/2 +
                self.animation_line_distaance_from_center + self.animation_line_size,
                self.get_size()[1]/2
            ), angle)

            painter.drawLine(point1[0], point1[1], point2[0], point2[1])

        painter.drawPoint(point1[0], point1[1])
        painter.end()

    def update_painter_angle(self):
        delta_angle = self.animation_rotating_speed * \
            (time.time() - self.animation_last_angle_update)
        self.animation_last_angle_update = time.time()
        self.animation_angle = (self.animation_angle +
                                delta_angle) % (360)

        # frame independent rotation speed
