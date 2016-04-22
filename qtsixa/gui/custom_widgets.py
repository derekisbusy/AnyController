#Embedded file name: /home/derek/Projects/QtSixA-1.5.1/qtsixa/gui/custom_widgets.py
from Crypto.Random.random import randint
from PyQt4.Qt import SIGNAL, SLOT, QTimer
from PyQt4.QtCore import Qt, QString, QTimeLine, QPointF, pyqtSignal, QThread
from PyQt4.QtGui import QPainter, QPen, QColor, QIcon, QDockWidget, QGraphicsEllipseItem, QGraphicsScene, QGraphicsView, QGraphicsItemAnimation, QGridLayout, QBrush, QPalette, qApp, QLabel, QPixmap, QGraphicsPixmapItem, QGraphicsDropShadowEffect, QHBoxLayout, QVBoxLayout, QProgressBar, QGraphicsItem, QGraphicsWidget, QApplication, QStyleFactory
import mmap
from multiprocessing import Process
import os
import posix_ipc
import pprint
import struct
import sys
from time import sleep
import utils
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


class QSixAxisThread(QThread):
    valueUpdated = pyqtSignal(int, int, int, int, int, int)

    def run(self):
        try:
            memory = posix_ipc.SharedMemory('sixaxis_controller_1')
            mapfile = mmap.mmap(memory.fd, memory.size)
            os.close(memory.fd)
            for i in range(0, 1000):
                sleep(0.1)
                i += 1
                s = utils.read_from_memory(mapfile, 100)
                a = struct.unpack('B', s[9])[0]
                z = struct.unpack('B', s[10])[0]
                x = struct.unpack('B', s[7])[0]
                y = struct.unpack('B', s[8])[0]
                b1 = struct.unpack('B', s[3])[0]
                b2 = struct.unpack('B', s[4])[0]
                b3 = struct.unpack('B', s[5])[0]
                l3 = 1 if b1 & 2 else 0
                r3 = 1 if b1 & 4 else 0
                self.valueUpdated.emit(x, y, a, z, l3, r3)
                print 'b1:%d b2:%d' % (b1, b2)

        except:
            e = sys.exc_info()[0]
            print 'Error: %s' % e


class TiggersView(QGraphicsView):

    def __init__(self, *args):
        QGraphicsView.__init__(self, *args)
        self.move(2, 22)
        self.btnSize = 60
        self.setMaximumHeight(60)
        self.setMaximumWidth(332)
        self.setMinimumHeight(60)
        self.setMinimumWidth(332)
        self.adjustSize()
        self.scene = QGraphicsScene(self)
        self.setStyleSheet('background-color:transparent; border-width: 0px; border: 0px;')
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)
        self.setScene(self.scene)


class BumpersView(QGraphicsView):

    def __init__(self, *args):
        QGraphicsView.__init__(self, *args)
        self.move(2, 22)
        self.btnSize = 60
        self.setMaximumHeight(60)
        self.setMaximumWidth(332)
        self.setMinimumHeight(60)
        self.setMinimumWidth(332)
        self.adjustSize()
        self.scene = QGraphicsScene(self)
        self.setStyleSheet('background-color:transparent; border-width: 0px; border: 0px;')
        self.l1 = QPixmap(os.getcwd() + '/../icons/l1.png')
        self.l1 = self.l1.scaled(self.btnSize, self.btnSize, Qt.KeepAspectRatio)
        self.l1Item = QGraphicsPixmapItem(self.l1)
        self.l1Item.setOffset(QPointF(30, 0))
        self.scene.addItem(self.l1Item)
        self.r1 = QPixmap(os.getcwd() + '/../icons/r1.png')
        self.r1 = self.l1.scaled(self.btnSize, self.btnSize, Qt.KeepAspectRatio)
        self.r1Item = QGraphicsPixmapItem(self.r1)
        self.r1Item.setOffset(QPointF(200, 0))
        self.scene.addItem(self.r1Item)
        self.setScene(self.scene)


class StartSelectView(QGraphicsView):

    def __init__(self, *args):
        QGraphicsView.__init__(self, *args)
        self.move(2, 250)
        self.btnSize = 28
        self.setMaximumHeight(self.btnSize * 2)
        self.setMaximumWidth(334)
        self.setMinimumHeight(self.btnSize * 2)
        self.setMinimumWidth(334)
        self.adjustSize()
        self.scene = QGraphicsScene(self)
        self.setStyleSheet('background-color:transparent; border-width: 0px; border: 0px;')
        self.psButtons = QPixmap(os.getcwd() + '/../icons/controller-sprite.png')
        self.select = self.psButtons.copy(696, 120, 45, 30)
        self.select = self.select.scaled(self.btnSize, self.btnSize, Qt.KeepAspectRatio)
        self.selectItem = QGraphicsPixmapItem(self.select)
        self.selectItem.setOffset(QPointF(0, 0))
        self.scene.addItem(self.selectItem)
        self.start = self.psButtons.copy(754, 120, 45, 30)
        self.start = self.start.scaled(self.btnSize, self.btnSize, Qt.KeepAspectRatio)
        self.startItem = QGraphicsPixmapItem(self.start)
        self.startItem.setOffset(QPointF(86, 0))
        self.scene.addItem(self.startItem)
        self.setScene(self.scene)


class DpadView(QGraphicsView):

    def __init__(self, *args):
        QGraphicsView.__init__(self, *args)
        self.move(2, 90)
        self.btnSize = 75
        self.padding = -35
        self.setMaximumHeight(self.btnSize * 2 + 20)
        self.setMaximumWidth(self.btnSize * 2 + 20)
        self.setMinimumHeight(self.btnSize * 2 + 20)
        self.setMinimumWidth(self.btnSize * 2 + 20)
        self.adjustSize()
        self.setStyleSheet('background-color:transparent; border-width: 0px; border: 0px;')
        self.scene = QGraphicsScene(self)
        self.left = QPixmap(os.getcwd() + '/../icons/left.png')
        self.left = self.left.scaled(self.btnSize, self.btnSize, Qt.KeepAspectRatio)
        self.right = QPixmap(os.getcwd() + '/../icons/right.png')
        self.right = self.right.scaled(self.btnSize, self.btnSize, Qt.KeepAspectRatio)
        self.up = QPixmap(os.getcwd() + '/../icons/up.png')
        self.up = self.up.scaled(self.btnSize, self.btnSize, Qt.KeepAspectRatio)
        self.down = QPixmap(os.getcwd() + '/../icons/down.png')
        self.down = self.down.scaled(self.btnSize, self.btnSize, Qt.KeepAspectRatio)
        self.leftItem = QGraphicsPixmapItem(self.left)
        self.leftItem.setOffset(QPointF(0, self.btnSize + self.padding))
        self.scene.addItem(self.leftItem)
        self.rightItem = QGraphicsPixmapItem(self.right)
        self.rightItem.setOffset(QPointF(self.btnSize * 2 + self.padding * 2, self.btnSize + self.padding))
        self.scene.addItem(self.rightItem)
        self.upItem = QGraphicsPixmapItem(self.up)
        self.upItem.setOffset(QPointF(self.btnSize + self.padding, 0))
        self.scene.addItem(self.upItem)
        self.downItem = QGraphicsPixmapItem(self.down)
        self.downItem.setOffset(QPointF(self.btnSize + self.padding, self.btnSize * 2 + self.padding * 2))
        self.scene.addItem(self.downItem)
        self.effect = QGraphicsDropShadowEffect()
        self.effect.setOffset(0, 0)
        self.effect.setBlurRadius(20)
        self.effect.setColor(Qt.green)
        self.downItem.setGraphicsEffect(self.effect)
        self.setScene(self.scene)
        self.tl2 = QTimeLine(10000)
        self.tl2.setFrameRange(0, 10000)
        self.t = QGraphicsItemAnimation()
        self.t.setItem(self.downItem)
        self.t.setTimeLine(self.tl2)
        self.tl2.connect(self.tl2, SIGNAL('frameChanged(int)'), self.updateEffect)
        self.effectd = 3
        self.tl2.start()

    def updateEffect(self):
        if self.effect.blurRadius() > 50:
            self.effectd = -3
        elif self.effect.blurRadius() < 5:
            self.effectd = 3
        self.effect.setBlurRadius(self.effect.blurRadius() + self.effectd)


class FaceButtonsView(QGraphicsView):

    def __init__(self, *args):
        QGraphicsView.__init__(self, *args)
        self.move(170, 90)
        self.btnSize = 40
        self.padding = 5
        self.setMaximumHeight(self.btnSize * 4)
        self.setMaximumWidth(self.btnSize * 4)
        self.setMinimumHeight(self.btnSize * 4)
        self.setMinimumWidth(self.btnSize * 4)
        self.adjustSize()
        self.setStyleSheet('background-color:transparent; border-width: 0px; border: 0px;')
        self.scene = QGraphicsScene(self)
        self.psButtons = QPixmap(os.getcwd() + '/../icons/PS3_Buttons.png')
        self.triangle = self.psButtons.copy(0, 0, 220, 225)
        self.triangle = self.triangle.scaled(self.btnSize, self.btnSize, Qt.KeepAspectRatio)
        self.square = self.psButtons.copy(220, 0, 220, 225)
        self.square = self.square.scaled(self.btnSize, self.btnSize, Qt.KeepAspectRatio)
        self.circle = self.psButtons.copy(440, 0, 220, 225)
        self.circle = self.circle.scaled(self.btnSize, self.btnSize, Qt.KeepAspectRatio)
        self.cross = self.psButtons.copy(660, 0, 220, 225)
        self.cross = self.cross.scaled(self.btnSize, self.btnSize, Qt.KeepAspectRatio)
        self.triangleItem = QGraphicsPixmapItem(self.triangle)
        self.triangleItem.setOffset(QPointF(self.btnSize + self.padding, 0))
        self.scene.addItem(self.triangleItem)
        self.squareItem = QGraphicsPixmapItem(self.square)
        self.squareItem.setOffset(QPointF(0, self.btnSize + self.padding))
        self.scene.addItem(self.squareItem)
        self.circleItem = QGraphicsPixmapItem(self.circle)
        self.circleItem.setOffset(QPointF(self.btnSize * 2 + self.padding * 2, self.btnSize + self.padding))
        self.scene.addItem(self.circleItem)
        self.crossItem = QGraphicsPixmapItem(self.cross)
        self.crossItem.setOffset(QPointF(self.btnSize + self.padding, self.btnSize * 2 + self.padding * 2))
        self.scene.addItem(self.crossItem)
        self.effect = QGraphicsDropShadowEffect()
        self.effect.setOffset(0, 0)
        self.effect.setBlurRadius(20)
        self.effect.setColor(Qt.green)
        self.triangleItem.setGraphicsEffect(self.effect)
        self.setScene(self.scene)
        self.tl2 = QTimeLine(10000)
        self.tl2.setFrameRange(0, 10000)
        self.t = QGraphicsItemAnimation()
        self.t.setItem(self.triangleItem)
        self.t.setTimeLine(self.tl2)
        self.tl2.connect(self.tl2, SIGNAL('frameChanged(int)'), self.updateEffect)
        self.effectd = 3
        self.tl2.start()

    def updateEffect(self):
        if self.effect.blurRadius() > 50:
            self.effectd = -3
        elif self.effect.blurRadius() < 5:
            self.effectd = 3
        self.effect.setBlurRadius(self.effect.blurRadius() + self.effectd)


class SixAxisView(QGraphicsView):

    def __init__(self, *args):
        QGraphicsView.__init__(self, *args)
        self.move(20, 240)
        self.outerD = 125
        self.innerD = 35
        self.innerRange = 48
        self.inputRange = 256
        self.thresh = 3
        self.padding = 40
        self.marginTop = 10
        self.worker = QSixAxisThread()
        self.worker.valueUpdated.connect(self.moveJoysticks)
        self.worker.start()
        self.setContentsMargins(0, 0, 0, 0)
        self.setMaximumHeight(180)
        self.setMaximumWidth(420)
        self.setMinimumHeight(240)
        self.setMinimumWidth(300)
        self.adjustSize()
        self.scene = QGraphicsScene(self)
        self.outerCircle1 = QGraphicsEllipseItem(0, self.marginTop, self.outerD, self.outerD)
        self.outerCircle1.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
        self.outerCircle1.setBrush(Qt.gray)
        self.innerCircle1 = QGraphicsEllipseItem(self.outerD / 2 - self.innerD / 2, self.outerD / 2 - self.innerD / 2 + self.marginTop, self.innerD, self.innerD)
        self.innerCircle1.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
        self.innerCircle1.setBrush(Qt.lightGray)
        self.scene.addItem(self.outerCircle1)
        self.scene.addItem(self.innerCircle1)
        self.outerCircle2 = QGraphicsEllipseItem(self.outerD + self.padding, self.marginTop, self.outerD, self.outerD)
        self.outerCircle2.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
        self.outerCircle2.setBrush(Qt.gray)
        self.innerCircle2 = QGraphicsEllipseItem(self.outerD + self.padding + self.outerD / 2 - self.innerD / 2, self.outerD / 2 - self.innerD / 2 + self.marginTop, self.innerD, self.innerD)
        self.innerCircle2.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
        self.innerCircle2.setBrush(Qt.lightGray)
        self.scene.addItem(self.outerCircle2)
        self.scene.addItem(self.innerCircle2)
        self.setScene(self.scene)
        self.setStyleSheet('background-color:transparent; border-width: 0px; border: 0px;')
        self.currentX = 0
        self.currentY = 0
        self.currentA = 0
        self.currentZ = 0
        self.psBtn = QPixmap(os.getcwd() + '/../icons/bt_PS.png')
        self.psBtn = self.psBtn.scaled(50, 50, Qt.KeepAspectRatio)
        self.psItem = QGraphicsPixmapItem(self.psBtn)
        self.psItem.setOffset(QPointF(self.outerD - 4, 0))
        self.effect = QGraphicsDropShadowEffect()
        self.effect.setOffset(0, 0)
        self.effect.setBlurRadius(20)
        self.effect.setColor(Qt.green)
        self.psItem.setGraphicsEffect(self.effect)
        self.scene.addItem(self.psItem)
        self.tl2 = QTimeLine(10000)
        self.tl2.setFrameRange(0, 10000)
        self.c = QGraphicsItemAnimation()
        self.c.setItem(self.psItem)
        self.c.setTimeLine(self.tl2)
        self.tl2.connect(self.tl2, SIGNAL('frameChanged(int)'), self.updateEffect)
        self.effectd = 3
        self.tl2.start()

    def updateEffect(self):
        if self.effect.blurRadius() > 50:
            self.effectd = -3
        elif self.effect.blurRadius() < 5:
            self.effectd = 3
        self.effect.setBlurRadius(self.effect.blurRadius() + self.effectd)

    def update(self, *args, **kwargs):
        return QGraphicsView.update(self, *args, **kwargs)

    def moveJoysticks(self, x, y, a, z, l3, r3):
        x2 = x * self.innerRange / self.inputRange - self.innerRange / 2
        y2 = y * self.innerRange / self.inputRange - self.innerRange / 2
        a2 = a * self.innerRange / self.inputRange - self.innerRange / 2
        z2 = z * self.innerRange / self.inputRange - self.innerRange / 2
        if -self.thresh <= x2 <= self.thresh:
            x2 = 0
        if -self.thresh <= y2 <= self.thresh:
            y2 = 0
        if -self.thresh <= a2 <= self.thresh:
            a2 = 0
        if -self.thresh <= z2 <= self.thresh:
            z2 = 0
        self.tl = QTimeLine(10)
        self.tl.setFrameRange(0, 10)
        self.a = QGraphicsItemAnimation()
        self.a.setItem(self.innerCircle1)
        self.a.setTimeLine(self.tl)
        self.a.setPosAt(0, QPointF(self.currentX, self.currentY))
        self.a.setTranslationAt(1, x2, y2)
        if l3:
            self.innerCircle1.setPen(QPen(QColor(Qt.white), 1, Qt.SolidLine))
            self.innerCircle1.setBrush(QColor(200, 225, 3))
        else:
            self.innerCircle1.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
            self.innerCircle1.setBrush(Qt.lightGray)
        if r3:
            self.innerCircle2.setPen(QPen(QColor(Qt.white), 1, Qt.SolidLine))
            self.innerCircle2.setBrush(QColor(200, 225, 3))
        else:
            self.innerCircle2.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
            self.innerCircle2.setBrush(Qt.lightGray)
        self.b = QGraphicsItemAnimation()
        self.b.setItem(self.innerCircle2)
        self.b.setTimeLine(self.tl)
        self.b.setPosAt(0, QPointF(self.currentA, self.currentZ))
        self.b.setTranslationAt(1, a2, z2)
        self.currentX = x2
        self.currentY = y2
        self.currentA = a2
        self.currentZ = z2
        self.tl.start()


class DualJoystickView(QGraphicsView):

    def __init__(self, *args):
        QGraphicsView.__init__(self, *args)
        self.outerD = 125
        self.innerD = 35
        self.innerRange = 48
        self.inputRange = 256
        self.thresh = 3
        self.padding = 40
        self.worker = QSixAxisThread()
        self.worker.valueUpdated.connect(self.moveJoysticks)
        self.worker.start()
        self.move(2, 100)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMaximumHeight(180)
        self.setMaximumWidth(420)
        self.setMinimumHeight(140)
        self.setMinimumWidth(300)
        self.adjustSize()
        self.scene = QGraphicsScene(self)
        self.outerCircle1 = QGraphicsEllipseItem(0, 0, self.outerD, self.outerD)
        self.outerCircle1.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
        self.outerCircle1.setBrush(Qt.gray)
        self.innerCircle1 = QGraphicsEllipseItem(self.outerD / 2 - self.innerD / 2, self.outerD / 2 - self.innerD / 2, self.innerD, self.innerD)
        self.innerCircle1.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
        self.innerCircle1.setBrush(Qt.lightGray)
        self.scene.addItem(self.outerCircle1)
        self.scene.addItem(self.innerCircle1)
        self.outerCircle2 = QGraphicsEllipseItem(self.outerD + self.padding, 0, self.outerD, self.outerD)
        self.outerCircle2.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
        self.outerCircle2.setBrush(Qt.gray)
        self.innerCircle2 = QGraphicsEllipseItem(self.outerD + self.padding + self.outerD / 2 - self.innerD / 2, self.outerD / 2 - self.innerD / 2, self.innerD, self.innerD)
        self.innerCircle2.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
        self.innerCircle2.setBrush(Qt.lightGray)
        self.scene.addItem(self.outerCircle2)
        self.scene.addItem(self.innerCircle2)
        self.setScene(self.scene)
        self.setStyleSheet('background-color:transparent;')
        self.currentX = 0
        self.currentY = 0
        self.currentA = 0
        self.currentZ = 0
        self.test = QGraphicsItem(self.outerCircle2)

    def moveJoysticks(self, x, y, a, z, l3, r3):
        x2 = x * self.innerRange / self.inputRange - self.innerRange / 2
        y2 = y * self.innerRange / self.inputRange - self.innerRange / 2
        a2 = a * self.innerRange / self.inputRange - self.innerRange / 2
        z2 = z * self.innerRange / self.inputRange - self.innerRange / 2
        if -self.thresh <= x2 <= self.thresh:
            x2 = 0
        if -self.thresh <= y2 <= self.thresh:
            y2 = 0
        if -self.thresh <= a2 <= self.thresh:
            a2 = 0
        if -self.thresh <= z2 <= self.thresh:
            z2 = 0
        self.tl = QTimeLine(10)
        self.tl.setFrameRange(0, 10)
        self.a = QGraphicsItemAnimation()
        self.a.setItem(self.innerCircle1)
        self.a.setTimeLine(self.tl)
        self.a.setPosAt(0, QPointF(self.currentX, self.currentY))
        self.a.setTranslationAt(1, x2, y2)
        if l3:
            self.innerCircle1.setPen(QPen(QColor(Qt.white), 1, Qt.SolidLine))
            self.innerCircle1.setBrush(QColor(200, 225, 3))
        else:
            self.innerCircle1.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
            self.innerCircle1.setBrush(Qt.lightGray)
        if r3:
            self.innerCircle2.setPen(QPen(QColor(Qt.white), 1, Qt.SolidLine))
            self.innerCircle2.setBrush(QColor(200, 225, 3))
        else:
            self.innerCircle2.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
            self.innerCircle2.setBrush(Qt.lightGray)
        self.b = QGraphicsItemAnimation()
        self.b.setItem(self.innerCircle2)
        self.b.setTimeLine(self.tl)
        self.b.setPosAt(0, QPointF(self.currentA, self.currentZ))
        self.b.setTranslationAt(1, a2, z2)
        self.currentX = x2
        self.currentY = y2
        self.currentA = a2
        self.currentZ = z2
        self.tl.start()


class SingleJoystickView(QGraphicsView):

    def __init__(self, *args):
        QGraphicsView.__init__(self, *args)
        self.outerD = 125
        self.innerD = 25
        self.innerRange = 50
        self.inputRange = 256
        self.thresh = 3
        self.worker = JoystickThread()
        self.worker.valueUpdated.connect(self.moveJoystick)
        self.worker.start()
        self.move(30, 100)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMaximumHeight(140)
        self.setMaximumWidth(140)
        self.adjustSize()
        self.scene = QGraphicsScene(self)
        self.outerCircle = QGraphicsEllipseItem(0, 0, self.outerD, self.outerD)
        self.outerCircle.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
        self.outerCircle.setBrush(Qt.gray)
        self.innerCircle = QGraphicsEllipseItem(self.outerD / 2 - self.innerD / 2, self.outerD / 2 - self.innerD / 2, self.innerD, self.innerD)
        self.innerCircle.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
        self.innerCircle.setBrush(Qt.lightGray)
        self.scene.addItem(self.outerCircle)
        self.scene.addItem(self.innerCircle)
        self.setScene(self.scene)
        self.setStyleSheet('background-color:transparent;color:red')
        self.currentX = 0
        self.currentY = 0

    def moveJoystick(self, x, y):
        x2 = x * self.innerRange / self.inputRange - self.innerRange / 2
        y2 = y * self.innerRange / self.inputRange - self.innerRange / 2
        if -self.thresh <= x2 <= self.thresh:
            x2 = 0
        if -self.thresh <= y2 <= self.thresh:
            y2 = 0
        self.tl = QTimeLine(10)
        self.tl.setFrameRange(0, 10)
        self.a = QGraphicsItemAnimation()
        self.a.setItem(self.innerCircle)
        self.a.setTimeLine(self.tl)
        self.a.setPosAt(0, QPointF(self.currentX, self.currentY))
        self.a.setTranslationAt(1, x2, y2)
        self.currentX = x2
        self.currentY = y2
        self.tl.start()
        print 'x:%d y:%d' % (x2, y2)


class JoystickThread(QThread):
    valueUpdated = pyqtSignal(int, int, int, int)

    def run(self):
        try:
            memory = posix_ipc.SharedMemory('sixaxis_controller_1')
            mapfile = mmap.mmap(memory.fd, memory.size)
            os.close(memory.fd)
            for i in range(0, 1000):
                sleep(0.1)
                i += 1
                s = utils.read_from_memory(mapfile, 100)
                x = struct.unpack('B', s[9])[0]
                y = struct.unpack('B', s[10])[0]
                self.valueUpdated.emit(int(x), int(y))

        except:
            e = sys.exc_info()[0]
            print 'Error: %s' % e


class InputDockWidget(QDockWidget):

    def __init__(self, *args):
        QDockWidget.__init__(self, *args)
        self.setupUi(self)
        self.setWindowIcon(QIcon(':/icons/qtsixa.png'))
        self.color = QColor(Qt.lightGray)
        self.setMinimumWidth(350)
        self.setContentsMargins(0, 0, 0, 0)
        self.adjustSize()

    def setupUi(self, QtSixAMainW):
        QtSixAMainW.setObjectName(_fromUtf8('QtSixAMainW'))
        QtSixAMainW.resize(935, 513)
        triggers = TiggersView(self)
        triggers.show()
        bumpers = BumpersView(self)
        bumpers.show()
        face = FaceButtonsView(self)
        face.show()
        dpad = DpadView(self)
        dpad.show()
        select = StartSelectView(self)
        select.show()
        sixaxis = SixAxisView(self)
        sixaxis.show()
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(triggers)
        hbox.addWidget(bumpers)
        hbox.addWidget(dpad)
        hbox.addWidget(face)
        hbox.addWidget(select)
        hbox.addWidget(sixaxis)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.progress = QProgressBar(self)
        self.progress.setGeometry(20, 2, 50, 20)
        self.progress.setTextVisible(False)
        self.progress.setOrientation(Qt.Vertical)
        self.progress.setValue(80)
        self.progress.move(60,28)
        self.progress.show()
        print self.style().objectName()
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

    def paintEvent(self, event = None):
        pass


class SpriteAnimation(object):

    def __init__(self, image_path, sprite_width, sprite_height, label):
        pixmap = QPixmap(image_path)
        width, height = pixmap.width(), pixmap.height()
        self.pixmaps = []
        for x in range(0, width, sprite_width):
            for y in range(0, height, sprite_height):
                self.pixmaps.append(pixmap.copy(x, y, sprite_width, sprite_height))

        self._current_frame = 0
        self.label = label

    def play(self, interval = 100):
        self._timer = QTimer(interval=interval, timeout=self._animation_step)
        self._timer.start()

    def _animation_step(self):
        self.label.setPixmap(self.pixmaps[self._current_frame])
        self.label.update()
        self._current_frame += 1
        if self._current_frame >= len(self.pixmaps):
            self._current_frame = 0