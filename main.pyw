
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QMovie, QFont, QPixmap
from PyQt5.QtCore import QBuffer, QByteArray, QThread
from parsethread import CParseThread
import qrc
from zigenpos import CZigenPos


 
class CMainWdg(QtWidgets.QWidget):
    def __init__(self):
        super(CMainWdg, self).__init__()
        self.initUi()
        

    def initUi(self):  

        ftWdg = QFont('微软雅黑')
        ftWdg.setPixelSize(15)
        self.setFont(ftWdg)
        self.queryThread = CParseThread()
        self.setWindowTitle('五笔字根查询')
        #self.setFixedSize(400, 300)
        self.lbGif = QtWidgets.QLabel()
        self.mvGif = QMovie()
        self.lbGif.setMovie(self.mvGif)
        self.mainVBL = QVBoxLayout()
        self.setLayout(self.mainVBL)       
        #bytesBuff = getZigenGif('/wbbmcx/tp/软.gif')
        self.qab = QByteArray()
        self.buff = QBuffer(self.qab)
        self.setGifBuff(self.buff)
        #self.queryBtn = QPushButton('查询')
        self.lbIntro = QLabel('用于汉字的五笔编码查询')

        self.mainVBL.addWidget(self.lbIntro)

        self.hblLeNeeddQuery = QHBoxLayout()
        self.lbQuery = QLabel('查:')

        self.leNeedQuery = QLineEdit()

        self.leNeedQuery.setFixedSize(60, 45)
        ftLeNeedQuery =  QFont('微软雅黑')
        ftLeNeedQuery.setPixelSize(30)
        self.leNeedQuery.setFont(ftLeNeedQuery)
        self.leNeedQuery.setMaxLength(1)

        self.lbWubiCodeKey = QLabel('五笔编码:')
        self.lbWubiCodeValue = QLabel('')
        self.lbWubiCodeValue.setMinimumWidth(60)

        self.lbWubiCodeValue.setFont(ftLeNeedQuery)

        self.lbGifKey = QLabel('拆解图:')

        self.hblLeNeeddQuery.addWidget(self.lbQuery)
        self.hblLeNeeddQuery.addWidget(self.leNeedQuery)
        self.hblLeNeeddQuery.addWidget(self.lbWubiCodeKey)
        self.hblLeNeeddQuery.addWidget(self.lbWubiCodeValue)
        self.hblLeNeeddQuery.addWidget(self.lbGifKey)
        self.hblLeNeeddQuery.addWidget(self.lbGif)
        self.hblLeNeeddQuery.addStretch()   

        self.mainVBL.addSpacing(10)
        self.mainVBL.addLayout(self.hblLeNeeddQuery)  

        self.lbZigenPic = QLabel()
       # self.pxZigen = QPixmap(":res/wubizg.png")
        self.lbZigenPic.setPixmap(QPixmap(":res/wubizg.png"))

        self.lb1 = QLabel(self.lbZigenPic)
        self.lb1.setPixmap(QPixmap(":res/1.png"))
        self.lb1.setVisible(False)
        self.lb2 = QLabel(self.lbZigenPic)
        self.lb2.setPixmap(QPixmap(':res/2.png'))
        self.lb2.setVisible(False)
        self.lb3 = QLabel(self.lbZigenPic)
        self.lb3.setPixmap(QPixmap(':res/3.png'))
        self.lb3.setVisible(False)
        self.lb4 = QLabel(self.lbZigenPic)
        self.lb4.setPixmap(QPixmap(':res/4.png'))
        self.lb4.setVisible(False)

        self.lbLine = QLabel()
        self.lbLine.setFixedHeight(1)
        self.lbLine.setStyleSheet('QLabel{border: none;background: grey}')

        self.mainVBL.addWidget(self.lbLine)
        self.mainVBL.addWidget(self.lbZigenPic)
        #self.mainVBL.addWidget(self.lb1)

   
        #self.set
       # self.queryBtn.clicked.connect(self.onQuery)
        self.leNeedQuery.textChanged.connect(self.onLeChanged)
        self.queryThread.started.connect(self.onThreadStarted)
        self.queryThread.finished.connect(self.onThreadFinished)
        
        #self.mainVBL.addWidget(self.queryBtn)
        #self.mainVBL.addWidget(self.lbGif)
        self.mainVBL.addStretch()
        
    def startQueryZigen(self, text: str):
        if len(text) == 0:
            return
        
        if ord(text[0]) < 0x4e00 or ord(text[0]) > 0x9fa5:
            return 
        if not self.queryThread.isRunning():            
            self.queryThread.setHanzi(text[0])
            self.queryThread.start()

    def onLeChanged(self, text:str):        
        self.startQueryZigen(text)


    def onThreadStarted(self):
        pass

    def onThreadFinished(self):
        oldHanzi = self.queryThread.getHanzi()
        newHanzi = self.leNeedQuery.text()
        if len(newHanzi) != 0 and oldHanzi != newHanzi[0]:
           self.startQueryZigen(newHanzi[0]) 
           return 

        lstResult = self.queryThread.getZigenResult()
        if len(lstResult) != 2:
            self.lbWubiCodeValue.setText('查询失败')
        if not lstResult[0]:
            self.lbWubiCodeValue.setText('查询失败')

        self.lbWubiCodeValue.setText(lstResult[1])  
        
        self.lb1.setVisible(False)
        self.lb2.setVisible(False)
        self.lb3.setVisible(False)
        self.lb4.setVisible(False)
        zigenPos = CZigenPos()
        for index, cZegen in enumerate(lstResult[1]):
            pos = zigenPos.getIconNumPos(cZegen, index)
            #self.lb1.move(pos['x'] , pos['y'])
           #zigenPixPos = self.lbZigenPic.pos()
            if index == 0:
                self.lb1.move(pos['x'] , pos['y'])
                self.lb1.setVisible(True)
            elif index == 1:
                self.lb2.move(pos['x'] , pos['y'])
                self.lb2.setVisible(True)
            elif index == 2:
                self.lb3.move(pos['x'] , pos['y'])
                self.lb3.setVisible(True)
            elif index == 3:
                self.lb4.move(pos['x'] , pos['y'])
                self.lb4.setVisible(True)
            elif index == 4:
                pass

        #self.
        lstResult =  self.queryThread.getZigenGifResult()  
        if len(lstResult) != 2:
            self.setGifBuff(QBuffer())
            return
        if not lstResult[0]:
            self.setGifBuff(QBuffer())
            return

        if type(lstResult[1]) != type(b''):
            self.setGifBuff(QBuffer())
            return None

        self.qab = QByteArray(lstResult[1])
        self.buff = QBuffer(self.qab)
        self.setGifBuff(self.buff)
    
    def onQuery(self):
        strHanzi = self.leNeedQuery.text()
        if len(strHanzi) == 0:
            return None
        strHanzi = strHanzi[0]
        bytesBuff = getZigenGif('/wbbmcx/tp/{0}.gif'.format(strHanzi))
        if type(bytesBuff) != type(b''):
            return None
        self.qab = QByteArray(bytesBuff)
        self.buff = QBuffer(self.qab)
        self.setGifBuff(self.buff)
        
    
    def setGifBuff(self, gifBuff : QBuffer):
        self.mvGif.stop()
        self.mvGif.setDevice(gifBuff)
        #self.mvGif.setFormat(b'gif89a')
        self.mvGif.start()



if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)

    mainWdg = CMainWdg()
    mainWdg.show()
    app.exec()
    #print(getHanziZigen(sys.argv[1]))
    

