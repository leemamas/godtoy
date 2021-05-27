# *_* coding : UTF-8 *_*
# author  ：  Leemamas
# 开发时间  ：  2021/5/28  2:11

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class TablePet(QWidget):
    def __init__(self):
        super(TablePet, self).__init__()


        self.is_follow_mouse = False
        self.mouse_drag_pos = self.pos()
        # 每隔一段时间做个动作
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.start(100)

        ##僵尸形态
        self.sharp=1
        ##皇帝的新衣
        self.clothes = ''
        self.clothes_key = 0
        self.wardrobe(self.sharp)

        self.initUi()
        self.tray()


    ##衣柜
    def wardrobe(self,key):

        default = 'source\Zombie\Zombie_'
        battle = 'source\ConeheadZombie\ConeheadZombie_'
        if key == 0:
            self.clothes=default
            ##TODO 根据文件数自动获取
            self.clothes_key=21
        else:
            self.clothes=battle
            self.clothes_key=20


    ##变身
    def transformation(self):
        if self.sharp==0:
            self.wardrobe(1)
            self.sharp=1
        else:
            self.wardrobe(0)
            self.sharp=0

    def randomAct(self):
        # 读取图片不同的地址，实现动画效果
        if self.key<self.clothes_key:
            self.key+=1
        else:
            self.key=0

        self.pic_url = self.clothes + str(self.key) + '.png'
        self.pm = QPixmap(self.pic_url)
        if not self.is_follow_mouse:
            # 实现行进效果
            if self.w>0:
                self.w-=2
            else:
                self.w=1400
            self.move(self.w, self.h)
        self.lbl.setPixmap(self.pm)



    def initUi(self):
        screen = QDesktopWidget().screenGeometry()
        self.w=1400
        self.h=800
        self.setGeometry(self.w,self.h,300,300)
        # self.setWindowTitle('mypet')
        self.lbl = QLabel(self)
        self.key=0
        self.pic_url=self.clothes+str(self.key)+'.png'
        self.pm = QPixmap(self.pic_url)
        self.lbl.setPixmap(self.pm)

        # 背景透明等效果
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show()
        # self.repaint()


    #系统托盘
    def tray(self):
        tp=QSystemTrayIcon(self)
        tp.setIcon(QIcon('source\Zombie\Zombie_0.png'))
        ation_quit= QAction('QUIT', self, triggered=self.quit)
        transformation= QAction('transformation', self, triggered=self.transformation)
        tpMenu=QMenu(self)
        tpMenu.addAction(ation_quit)
        tpMenu.addAction(transformation)
        tp.setContextMenu(tpMenu)
        tp.show()

    #鼠标事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            xy=self.pos()
            self.w,self.h=xy.x(),xy.y()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def quit(self):
        self.close()
        sys.exit()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    myPet=TablePet()
    sys.exit(app.exec_())