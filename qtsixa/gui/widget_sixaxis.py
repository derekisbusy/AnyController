
from Crypto.Random.random import randint
from PyQt4.Qt import SIGNAL, SLOT, QTimer
from PyQt4.QtCore import Qt, QString, QTimeLine, QPointF, pyqtSignal, QThread
from PyQt4.QtGui import QPainter, QPen, QColor, QIcon, QDockWidget, QGraphicsEllipseItem, QGraphicsScene, QGraphicsView, QGraphicsItemAnimation, QGridLayout, QBrush, QPalette, qApp, QLabel, QPixmap, QGraphicsPixmapItem, QGraphicsDropShadowEffect, QHBoxLayout, QVBoxLayout, QProgressBar, QGraphicsItem, QGraphicsWidget, QApplication, QStyleFactory,\
    QGraphicsRectItem, QWidget
from fileinput import filename
from math import sqrt
import mmap
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
    def __init__(self, controller):
        QThread.__init__(self)
        self.controller = controller
    input = pyqtSignal(int,int,int,int,int,int,int,int,int,int,int,int,int,int,int,int,int,int,int,int,int)
    
#     input = pyqtSignal(['QString'])

    def run(self):
        try:
            memory = posix_ipc.SharedMemory('sixaxis_controller_1')
            mapfile = mmap.mmap(memory.fd, memory.size)
            os.close(memory.fd)
#             for i in range(0, 1000):
            while True :
                sleep(0.1)
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
                start = 1 if b1 & 0x08 else 0
                select = 1 if b1 & 0x01 else 0
                ps = 1 if b3 & 0x01 else 0
                up = struct.unpack('B', s[15])[0]
                right = struct.unpack('B', s[16])[0]
                down = struct.unpack('B', s[17])[0]
                left = struct.unpack('B', s[18])[0]
                l2 = struct.unpack('B', s[19])[0]
                r2 = struct.unpack('B', s[20])[0]
                l1 = struct.unpack('B', s[21])[0]
                r1 = struct.unpack('B', s[22])[0]
                tri = struct.unpack('B', s[23])[0]
                cir = struct.unpack('B', s[24])[0]
                cro = struct.unpack('B', s[25])[0]
                squ = struct.unpack('B', s[26])[0]
                self.input.emit(a,z,x,y,l3,r3,start,select,ps,up,right,down,left,tri,cir,squ,cro,l2,r2,l1,r1)
#                 self.controller.update()
#                 print 'b1:%d b2:%d' % (b1, b2)

        except:
            e = sys.exc_info()[0]
            print 'Error: %s' % e
            
class Button(QWidget):
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    
    def __init__(self, filename=None, width=None, height=None, x=0, y=0, pixmap=None, group=None, pos=None, size=None, padding=None):
        self.effects = {}
        self.animations = {}
        self.filename = filename if isinstance(filename, str) else None
        if pixmap :
            self.pixmap = pixmap
        elif isinstance(filename, QPixmap) :
            self.pixmap = filename
        elif isinstance(filename, str) :
            self.pixmap = QPixmap(os.path.dirname(__file__) + '/../buttons/' + filename)
        else :
            self.pixmap = None
        if (width != None or height != None) and self.pixmap != None :
            self.pixmap = self.pixmap.scaled(width if width != None else height,
                                     height if height != None else width, Qt.KeepAspectRatio)
        self.group = group
        self.pos = pos
        self.size = size
        self.padding = padding
        self.x = x
        self.y = y
        
        if isinstance(self.pixmap, QPixmap) :
            self.item = QGraphicsPixmapItem(self.pixmap)
            self.item.setOffset(QPointF(self.getX(), self.getY()))
            self.effect = QGraphicsDropShadowEffect()
            self.effect.setOffset(0, 0)
            self.effect.setBlurRadius(0)
            self.effect.setColor(Qt.green)
            self.addEffect('shadow', self.effect, True)
            self.addAnimation('glow', Glow(15, 300, self, maxRadius=80, minRadius=5))
#             self.item.setGraphicsEffect(effect)
#             self.tl = QTimeLine(10000)
#             self.t = QGraphicsItemAnimation()
#             self.t.setItem(self.item)
#             self.t.setTimeLine(self.tl)
#             self.tl.connect(self.tl, SIGNAL('frameChanged(int)'), self.test)
#             self.tl.start()
#             print 'added'
    def test(self):
        print 1
    def getX(self):
        x = self.x
        if self.group != None :
            x += self.group.x
        if self.pos != None :
            x += self.getPositionX()
        return x
    
    def getY(self):
        y = self.y
        if self.group != None :
            y += self.group.getY()
        if self.pos != None :
            y += self.getPositionY()
        return y
    
    def getPositionX(self):
        if self.pos == Button.TOP or self.pos == Button.BOTTOM:
            return self.getSize() + self.getPadding() if self.getCols() > 1 else 0
        elif self.pos == Button.RIGHT :
            return self.getSize() * (self.getCols() - 1) + self.getPadding() * (self.getCols() - 1)
        elif self.pos == Button.LEFT :
            return 0
    
    def getPositionY(self):
        if self.pos == Button.LEFT or self.pos == Button.RIGHT:
            return self.getSize() + self.getPadding() if self.getRows() > 1 else 0
        elif self.pos == Button.BOTTOM :
            return self.getSize() * (self.getRows() - 1) + self.getPadding() * (self.getRows() - 1)
        elif self.pos == Button.TOP :
            return 0
    
    def getSize(self):
        if self.size != None : 
            return self.size
        if isinstance(self.group, ButtonGroup) :
            return self.group.getSize()
        return 0
    
    def getPadding(self):
        if self.padding != None :
            return self.padding
        if isinstance(self.group, ButtonGroup) :
            return self.group.getPadding()
        return 0
    
    def getRows(self):
        if isinstance(self.group, ButtonGroup) :
            return self.group.getRows()
        return 1;
    def getCols(self):
        if isinstance(self.group, ButtonGroup) :
            return self.group.getCols()
        return 1;
    
    def addEffect(self, name, effect, show=True):
        self.effects[name] = effect
        if show :
            self.setEffect(name)
    
    def setEffect(self, name):
        self.item.setGraphicsEffect(self.effects[name])
    
    def setScene(self, scene):
        self.scene = scene
        self.scene.addItem(self.item)
    
    def addAnimation(self, name, animation):
        self.animations[name] = animation
    
    def play(self, name):
        print 'start'
        self.animations[name].start()
    
    def update(self, pressed):
        if pressed :
            print 'pressed'
            self.play('glow')

class RButton(Button):
    def getY(self):
        return 0

class Animation:
    def __init__(self, duration, component):
        self.tl = QTimeLine(duration)
        self.tl.setFrameRange(0, duration)
        self.component = component
        self.t = QGraphicsItemAnimation()
        self.t.setItem(self.component.item)
        self.t.setTimeLine(self.tl)
        self.tl.connect(self.tl, SIGNAL('frameChanged(int)'), self.update)
        self.tl.connect(self.tl, SIGNAL('finished()'), self.finished)
    def start(self):
        self.tl.stop()
        self.tl.start()
    def update(self):
        pass
    def finished(self):
        pass

class Glow(Animation):
    def __init__(self, speed, duration, component, maxRadius=50, minRadius=5, repeat=0):
        Animation.__init__(self, duration, component)
        self.speed = speed
        self.maxRadius = maxRadius
        self.minRadius = minRadius
        self.repeat = repeat
        self.d = speed
        if self.repeat :
            self.tl.setLoopCount(repeat)
    def start(self):
        self.component.effect.setBlurRadius(80)
        Animation.start(self)
    def update(self):
        if self.component.effect.blurRadius() > self.maxRadius:
            self.d = self.speed * -1
        elif self.component.effect.blurRadius() < self.minRadius:
            self.d = self.speed
        self.component.effect.setBlurRadius(self.component.effect.blurRadius() + self.d)
    def finished(self):
        self.component.effect.setBlurRadius(0)
class ButtonGroup:
    x = 0
    y = 0
    def __init__(self, x, y, size=20, padding=5, rows=3, cols=3):
        self.x = x
        self.y = y
        self.size = size
        self.padding = padding
        self.rows = rows
        self.cols = cols
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getSize(self):
        return self.size
    def getPadding(self):
        return self.padding
    def getRows(self):
        return self.rows
    def getCols(self):
        return self.cols

class Meterbar(Button):
    def __init__(self, max=255, filename=None, width=None, height=None, x=0, y=0, pixmap=None, group=None, pos=None, size=None, padding=None):
        Button.__init__(self, filename, width, height, x, y, pixmap, group, pos, size, padding)
        self.max = max
        self.outer = QGraphicsRectItem(x,y,width,max + 2)
        self.outer.setPen(QPen(QColor(Qt.black), 1, Qt.SolidLine))
        self.outer.setBrush(Qt.green)
#         self.outer.hide()
        self.inner = QGraphicsRectItem(x + 1,y + 1,width - 2,max)
        self.inner.setPen(QPen(QColor(Qt.green), 1, Qt.SolidLine))
        self.inner.setBrush(Qt.blue)
        self.items = [self.outer, self.inner]
        self.current = 255
        self.effect = QGraphicsDropShadowEffect()
        self.effect.setOffset(0, 0)
        self.effect.setBlurRadius(0)
        self.effect.setColor(Qt.green)
        self.item = self.outer
        self.addEffect('shadow', self.effect, True)
        self.addAnimation('glow', Glow(15, 300, self, maxRadius=80, minRadius=5))
#         self.test(10)
    
    def test(self, x):
        self.tl = QTimeLine(10000)
        self.tl.setFrameRange(0, 10000)
        self.a = QGraphicsItemAnimation()
        self.a.setItem(self.inner)
        self.a.setTimeLine(self.tl)
#         self.a.setPosAt(0, QPointF(self.getX(), self.current))
#         self.a.setTranslationAt(1, self.getX(), self.getY() + self.max - x + 1)
        self.a.setScaleAt(0, 1, 1)
        self.a.setScaleAt(1, 1, 0.1)
        self.current = x
        self.tl.start()
        
    def update(self, x):
        x2 = 1 - (float(x) * 1.0 / float(self.max))
#         print x
#         return
        self.tl = QTimeLine(10)
        self.tl.setFrameRange(0, 10)
        self.a = QGraphicsItemAnimation()
        self.a.setItem(self.inner)
        self.a.setTimeLine(self.tl)
#         self.a.setPosAt(0, QPointF(self.getX(), self.current))
#         self.a.setTranslationAt(1, self.getX(), self.getY() + self.max - x + 1)
        self.a.setScaleAt(0, 1, self.current)
        self.a.setScaleAt(1, 1, x2)
        self.current = x
        self.tl.start()
        if x > 3 :
            self.play('glow')
        
    def setScene(self, scene):
        self.scene = scene
        for item in self.items :
            self.scene.addItem(item)
        
class Joystick(Button):
    def __init__(self, outer, inner, filename=None, width=None, height=None, x=0, y=0, pixmap=None, group=None, pos=None, size=None, padding=None):
        Button.__init__(self, filename, width, height, x, y, pixmap, group, pos, size, padding)
        self.outer = outer
        self.inner = inner
        self.innerRange = 48
        self.inputRange = 256
        self.thresh = 5
        self.outerCircle = QGraphicsEllipseItem(self.getX(), self.getY(), self.outer, self.outer)
        self.outerCircle.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
        self.outerCircle.setBrush(Qt.gray)
        self.innerCircle = QGraphicsEllipseItem(self.getX() + self.outer / 2 - self.inner / 2, self.getY() + self.outer / 2 - self.inner / 2, self.inner, self.inner)
        self.innerCircle.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
        self.innerCircle.setBrush(Qt.lightGray)
        self.currentX = 0
        self.currentY = 0
        self.items = [self.outerCircle, self.innerCircle]
    def getItems(self):
        return self.items
    def setScene(self, scene):
        self.scene = scene
        for item in self.items :
            self.scene.addItem(item)
    def update(self,x,y,z):
#         y = y - sqrt(x + y) if x > 0 else y
#         x = x - sqrt(x + y) if y > 0 else x
        x2 = x * self.innerRange / self.inputRange - self.innerRange / 2
        y2 = y * self.innerRange / self.inputRange - self.innerRange / 2
        x2 = x2 - sqrt(abs(y2)) if x2 >= 0 else x2 + sqrt(abs(y2))
        y2 = y2 - sqrt(abs(x2)) if y2 >= 0 else y2 + sqrt(abs(x2)) 
        if self.inputRange / 2 - self.thresh <= x <= self.inputRange / 2 + self.thresh:
            x2 = 0
        if self.inputRange / 2 - self.thresh <= y <= self.inputRange / 2 + self.thresh:
            y2 = 0
        self.tl = QTimeLine(10)
        self.tl.setFrameRange(0, 10)
        self.a = QGraphicsItemAnimation()
        self.a.setItem(self.innerCircle)
        self.a.setTimeLine(self.tl)
        self.a.setPosAt(0, QPointF(self.currentX, self.currentY))
        self.a.setTranslationAt(1, x2, y2)
        if z:
            self.innerCircle.setPen(QPen(QColor(Qt.white), 1, Qt.SolidLine))
            self.innerCircle.setBrush(QColor(200, 225, 3))
        else:
            self.innerCircle.setPen(QPen(QColor(Qt.darkGray), 1, Qt.SolidLine))
            self.innerCircle.setBrush(Qt.lightGray)
        self.currentX = x2
        self.currentY = y2
        self.tl.start()

class ControllerView(QGraphicsView):
    def __init__(self, *args):
        QGraphicsView.__init__(self, *args)
    def addButton(self):
        return

class PS3ControllerView(ControllerView):
    def __init__(self, *args):
        ControllerView.__init__(self, *args)
        self.setStyleSheet('background-color:transparent; border-width: 0px; border: 0px;')
        self.setMinimumHeight(500)
        self.setMaximumHeight(500)
        self.setMinimumWidth(400)
        self.setMaximumWidth(400)
        self.setContentsMargins(0, 0, 0, 0)
        self.adjustSize()
        
        bumpers = ButtonGroup(20,0,75,0,1)
        facebtns = ButtonGroup(160,70,35,0)
        dpad = ButtonGroup(0,60,25,0)
        midbtns = ButtonGroup(80,170,40,0)
        js = ButtonGroup(0,180,75,0)
        facesprite = QPixmap(os.path.dirname(__file__) + '/../buttons/PS3_Buttons.png')
        sprite = QPixmap(os.path.dirname(__file__) + '/../icons/controller-sprite.png')
        self.btns = Map({'l1' : Button('l1.png', group=bumpers, pos=Button.LEFT),
                     'r1' : Button('r1.png', group=bumpers, pos=Button.RIGHT),
                     'r2' : Meterbar(255, width=5, x=270),
                     'l2' : Meterbar(255, width=5),
                     'select' : Button(sprite.copy(696, 120, 45, 30), group=midbtns, pos=Button.LEFT, width=34),
                     'start' : Button(sprite.copy(754, 120, 45, 30), group=midbtns, pos=Button.RIGHT, width=34),
                     'ps' : Button('ps.png', group=midbtns, pos=Button.BOTTOM, width=35),
                     'up' : Button('up.png', group=dpad, pos=Button.TOP),
                     'right' : Button('right.png', group=dpad, pos=Button.RIGHT),
                     'down' : Button('down.png', group=dpad, pos=Button.BOTTOM),
                     'left' : Button('left.png', group=dpad, pos=Button.LEFT),
                     'tri' : Button(facesprite.copy(0, 0, 220, 225), group=facebtns, pos=Button.TOP, width=35), 
                     'cir' : Button(facesprite.copy(440, 0, 220, 225), group=facebtns, pos=Button.RIGHT, width=35), 
                     'squ' : Button(facesprite.copy(220, 0, 220, 225), group=facebtns, pos=Button.LEFT, width=35), 
                     'cro' : Button(facesprite.copy(660, 0, 220, 225), group=facebtns, pos=Button.BOTTOM, width=35),})
        self.joysticks = Map({'left': Joystick(125, 40, group=js, pos=Button.LEFT), 'right': Joystick(125, 40, group=js, pos=Button.RIGHT)})
        self.scene = QGraphicsScene(self)
        for btn in self.btns.itervalues() :
            btn.setScene(self.scene)
        for joystick in self.joysticks.itervalues() :
            joystick.setScene(self.scene)

        self.setScene(self.scene)
        self.worker = QSixAxisThread(self)
        self.worker.input.connect(self.update)
        self.worker.start()
        
    def update(self, a,z,x,y,l3,r3,start,select,ps,up,right,down,left,tri,cir,squ,cro,l2,r2,l1,r1):
        self.joysticks['left'].update(x,y,l3)
        self.joysticks['right'].update(a,z,r3)
        print 'x:%d y:%d tri:%d' % (x, y, cir)
        self.btns['up'].update(up)
        self.btns['right'].update(right)
        self.btns['down'].update(down)
        self.btns['left'].update(left)
        self.btns['tri'].update(tri)
        self.btns['cir'].update(cir)
        self.btns['squ'].update(squ)
        self.btns['cro'].update(cro)
        self.btns['start'].update(start)
        self.btns['select'].update(select)
        self.btns['ps'].update(ps)
        self.btns['l1'].update(l1)
        self.btns['r1'].update(r1)
        self.btns['r2'].update(r2)
        self.btns['l2'].update(l2)
        return
        

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
        controller = PS3ControllerView(self)
        controller.show()
        print self.style().objectName()
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

    def paintEvent(self, event = None):
        pass


class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]