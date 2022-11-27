from PyQt5.QtCore import QThread
import funNetwork
import ptvsd

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
        #ptvsd.debug_this_thread()
        strZiGenAndImg = funNetwork.getHanziZigen(self.hanzi)
        if strZiGenAndImg[0] != None:
            self.resultZigen = [True, strZiGenAndImg[0]]
        else:
            self.resultZigen = [False, ""] 
        
        if strZiGenAndImg[1] != None:            
            bytesBuff = funNetwork.getZigenGif(strZiGenAndImg[1] )
            if bytesBuff != None:
                self.resultZigenGif = [True, bytesBuff]
            else:
                self.resultZigenGif = [False, b'']
        else:
            self.resultZigenGif = [False, b'']
            
    def getZigenResult(self):
        return self.resultZigen
    def getZigenGifResult(self):
        return self.resultZigenGif    