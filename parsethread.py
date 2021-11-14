from PyQt5.QtCore import QThread
import funNetwork

class CParseThread(QThread):
    def __init__(self):
        super(CParseThread, self).__init__()
        self.resultZigen = [False, '']
        self.resultZigenGif = [False, b'']
    
    def setHanzi(self, strHanzi : str):
        self.hanzi = strHanzi
        
    def getHanzi(self):
        return self.hanzi
       
    def run(self):
        strZiGen = funNetwork.getHanziZigen(self.hanzi)
        if strZiGen != None:
            self.resultZigen = [True, strZiGen]
        else:
            self.resultZigen = [False, ""] 

        bytesBuff = funNetwork.getZigenGif('/wbbmcx/tp/{0}.gif'.format(self.hanzi))
        if bytesBuff != None:
            self.resultZigenGif = [True, bytesBuff]
        else:
            self.resultZigenGif = [False, b'']
            
    def getZigenResult(self):
        return self.resultZigen
    def getZigenGifResult(self):
        return self.resultZigenGif    