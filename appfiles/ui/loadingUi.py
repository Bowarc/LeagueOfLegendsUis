from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QShortcut
from PyQt5.QtGui import QKeySequence, QPixmap, QFont, QPainter, QColor, QPen, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QPoint

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
        self.animation_line_size = 12
        self.animation_line_distaance_from_center = 280
        self.animation_line_color = "#252929"
        self.animation_rotating_speed = 5  # degree per seccond
        self.animation_last_angle_update = time.time()

        self.animation_painterUpdateTimer = QTimer(self)
        self.animation_painterUpdateTimer.timeout.connect(self.update)
        self.animation_painterUpdateTimer.start(0)

        # init the outer lines
        self.outer_lines_size = 250
        self.outer_lines_distance_from_center = 500

        # init the diamonds
        self.diamond_vertical_size = 10
        self.diamond_horizontal_size = 10
        self.diamond_distance_from_center = 490 - self.diamond_vertical_size

        # progress bar update
        self.progressUpdateTimer = QTimer(self)
        self.progressUpdateTimer.timeout.connect(self.update_progress_bar)
        self.progressUpdateTimer.start(0)

    def setupUi(self):
        self.setObjectName("Window")

        logo_size = (501, 199)
        logo_pos = (self.get_size()[0]/2-logo_size[0]/2 + 10,
                    self.get_size()[1]/2-logo_size[1]/2 - 40)

        self.logoLabel = QtWidgets.QLabel(self)
        self.logoLabel.setGeometry(QtCore.QRect(
            logo_pos[0], logo_pos[1], logo_size[0], logo_size[1]))
        self.logoLabel.setPixmap(QtGui.QPixmap(
            QPixmap(self.assetsLoader.getImage("LeagueOfLinux.png"))))
        self.logoLabel.setObjectName("logo")

        loading_size = (110, 30)
        loading_pos = (self.get_size()[0]/2 - loading_size[0] / 2,
                       self.get_size()[1]/2 - loading_size[1] / 2 + 100)
        self.loadingLabel = QtWidgets.QLabel("LOADING", self)
        self.loadingLabel.setGeometry(QtCore.QRect(
            loading_pos[0], loading_pos[1], loading_size[0], loading_size[1]))
        self.loadingLabel.setObjectName("loadingText")

        loadingBar_size = (
            200, 11
        )
        loadingBar_pos = (
            self.get_size()[0]/2 - loadingBar_size[0]/2,
            self.get_size()[1]/2 - loadingBar_size[1]/2 + 120,
        )
        self.loadingBar = QtWidgets.QProgressBar(self)
        self.loadingBar.setGeometry(QtCore.QRect(
            loadingBar_pos[0], loadingBar_pos[1], loadingBar_size[0], loadingBar_size[1]))
        self.loadingBar.setMaximum(1000)
        self.loadingBar.setValue(0)
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
        painter.setRenderHint(QPainter.Antialiasing, True)

        # center of the window
        origin = (self.get_size()[0]/2, self.get_size()[1]/2)

        # draw the rotating animation
        ray_number = 200
        for i in range(ray_number):
            pen = QPen(QColor("#1b1d1d"), 1.5, Qt.SolidLine)
            painter.setPen(pen)

            angle = self.animation_angle + (i + 0.5) * (360 / ray_number)
            point1 = physics.rotate_point(origin, QPoint(
                self.get_size()[0]/2 +
                self.animation_line_distaance_from_center,
                self.get_size()[1]/2
            ), angle)

            point2 = physics.rotate_point(origin, QPoint(
                self.get_size()[0]/2 +
                self.animation_line_distaance_from_center + self.animation_line_size,
                self.get_size()[1]/2
            ), angle)

            painter.drawLine(point1.x(), point1.y(), point2.x(), point2.y())

        # draw the outer lines
        outer_ray_number = 150
        for i in range(outer_ray_number):
            angle = (i + 0.5) * (360 / outer_ray_number)
            point1 = physics.rotate_point(origin, QPoint(
                self.get_size()[0]/2 +
                self.outer_lines_distance_from_center,
                self.get_size()[1]/2
            ), angle)

            point2 = physics.rotate_point(origin, QPoint(
                self.get_size()[0]/2 +
                self.outer_lines_distance_from_center + self.outer_lines_size,
                self.get_size()[1]/2
            ), angle)
            circle_gradient = QLinearGradient(QtCore.QPoint(
                point1.x(), point1.y()), QtCore.QPoint(point2.x(), point2.y()))
            circle_gradient.setColorAt(0, QColor("#2e3333"))
            circle_gradient.setColorAt(1, QColor("#181b1b"))
            pen = QtGui.QPen(
                QColor(self.animation_line_color), 0.20, Qt.SolidLine)
            pen.setBrush(circle_gradient)
            painter.setPen(pen)
            painter.drawLine(point1.x(), point1.y(), point2.x(), point2.y())

        # draw the circle
        size = self.animation_line_distaance_from_center + self.animation_line_size + 10

        point1 = (
            self.get_size()[0]/2-size, self.get_size()[1]/2-size
        )

        point2 = (
            self.get_size()[0]/2+size, self.get_size()[1]/2+size
        )
        circle_gradient = QLinearGradient(QtCore.QPoint(
            point1[0]-500, point1[1] + size), QtCore.QPoint(point2[0] + 500, point2[1] - size))
        cc0 = QColor("#140f06")
        cc1 = QColor("#231b0b")
        cc2 = QColor("#362a11")
        cc3 = QColor("#675531")
        cc4 = QColor("#806a3e")
        cc5 = QColor("#d0ae67")
        # cc6 = QColor("#dabf86")
        circle_gradient.setColorAt(0, cc1)
        circle_gradient.setColorAt(0.25, cc3)
        circle_gradient.setColorAt(0.30, cc5)

        circle_gradient.setColorAt(0.33, cc2)
        circle_gradient.setColorAt(0.67, cc2)

        circle_gradient.setColorAt(0.70, cc5)
        circle_gradient.setColorAt(0.75, cc3)
        circle_gradient.setColorAt(1, cc1)

        pen = QtGui.QPen(QColor(0, 0, 0,), 2.5, Qt.SolidLine,
                         Qt.RoundCap, Qt.RoundJoin)
        pen.setBrush(circle_gradient)
        painter.setPen(pen)

        painter.drawEllipse(point1[0], point1[1], point2[0] -
                            point1[0], point2[1] - point1[1])
        # painter.drawRect(point1[0], point1[1], point2[0] -
        #                  point1[0], point2[1] - point1[1])

        pen = QtGui.QPen(QColor(0, 0, 0,), 1, Qt.SolidLine,
                         Qt.RoundCap, Qt.RoundJoin)
        pen.setBrush(circle_gradient)
        painter.setPen(pen)

        line_size = 500
        line = (point1[0], self.get_size()[1]/2,
                point1[0]-line_size, self.get_size()[1]/2)
        painter.drawLine(line[0], line[1], line[2], line[3])

        line2 = (point2[0], self.get_size()[1]/2,
                 point2[0]+line_size, self.get_size()[1]/2)
        painter.drawLine(line2[0], line2[1], line2[2], line2[3])

        # draw diamonds
        diamond_number = 22
        diamond_template = [
            QPoint(-self.diamond_vertical_size/2, 0),
            QPoint(0, +self.diamond_horizontal_size/2),
            QPoint(+self.diamond_vertical_size/2, 0),
            QPoint(0, -self.diamond_horizontal_size/2),
        ]
        pen = QtGui.QPen(QColor("#806a3e"), 1.5, Qt.SolidLine,
                         Qt.RoundCap, Qt.RoundJoin)

        gradient = QLinearGradient(QtCore.QPoint(
            self.get_size()[0]/2, 0), QtCore.QPoint(self.get_size()[0]/2, self.get_size()[1]))
        dc0 = QColor("#140f06")
        # dc1 = QColor("#231b0b")
        # dc2 = QColor("#362a11")
        dc3 = QColor("#675531")
        dc4 = QColor("#806a3e")
        dc5 = QColor("#d0ae67")
        # dc6 = QColor("#dabf86")
        gradient.setColorAt(0, dc0)
        gradient.setColorAt(0.25, dc3)
        gradient.setColorAt(0.30, dc4)

        gradient.setColorAt(0.33, dc5)
        gradient.setColorAt(0.67, dc5)

        gradient.setColorAt(0.70, dc4)
        gradient.setColorAt(0.75, dc3)
        gradient.setColorAt(1, dc0)

        pen.setBrush(gradient)
        painter.setPen(pen)
        for i in range(diamond_number):
            angle = (i + 0.5) * (360 / diamond_number)
            diamond_middle = physics.rotate_point(origin, QPoint(
                self.get_size()[0]/2 +
                self.diamond_distance_from_center + self.diamond_vertical_size/2,
                self.get_size()[1]/2
            ), angle)

            new_diamond = physics.process_diamond(
                diamond_template, diamond_middle)

            rotated_new_diamond = []
            for point in new_diamond:
                rotated_new_diamond.append(
                    physics.rotate_point(
                        (diamond_middle.x(), diamond_middle.y()), point, angle)
                )
            painter.drawPolyline(*rotated_new_diamond)

        # pen = QtGui.QPen(QColor("#d0ae67"), 1, Qt.SolidLine,
        #                  Qt.RoundCap, Qt.RoundJoin)
        # painter.setPen(pen)
        # spacing = 50
        # # QtCore.QPoint(50, 20)
        # diamond_pos = QPoint(100, 100)
        # # print(diamond_pos.x())
        # newDiamond = physics.process_diamond(diamond_template, diamond_pos)
        # painter.drawPolyline(
        #     *newDiamond)

        painter.end()

    def update_painter_angle(self):
        delta_angle = self.animation_rotating_speed * \
            (time.time() - self.animation_last_angle_update)
        self.animation_last_angle_update = time.time()
        self.animation_angle = (self.animation_angle +
                                delta_angle) % (360)

        # frame independent rotation speed
    def update_progress_bar(self):
        self.loadingBar.setValue(self.loadingBar.value()+1)
        # if self.loadingBar.value() == self.loadingBar.maximum():
        #     self.close()
