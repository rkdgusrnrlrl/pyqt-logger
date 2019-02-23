from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import logging
from time import sleep

import sys
from os import path

sys.path.append(path.dirname(path.abspath(path.dirname(__file__))))
from logger import logger
    
 
class TestThread(QThread, logging.StreamHandler):
    threadEvent = QtCore.pyqtSignal(str)
 
    def __init__(self, parent=None):
        super().__init__()
        logging.StreamHandler.__init__(self)
        
        self._logger = logger
        self._logger.addHandler(self)

        self.main = parent
        self.isRun = False

    def info(self, msg):
        self.threadEvent.emit(str(msg))

    def emit(self, record):
        msg = self.format(record)
        self.threadEvent.emit(str(msg))
 
    def run(self):
        cnt = 0
        while True:
            if not self.isRun:
                break

            self._logger.info('hello %d' % cnt)
            cnt += 1
            sleep(2)
        
 
 
class TestGUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
 
        self.btn1 = QPushButton("thread start", self)
        self.btn2 = QPushButton("thread stop", self)
 
        vertBox = QVBoxLayout()
        vertBox.addWidget(self.btn1)
        vertBox.addWidget(self.btn2)
        self.setLayout(vertBox)
        # 1600 * 1200
        self.setGeometry(0, 1000, 1600, 160)
 
        self.btn1.clicked.connect(self.threadStart)
        self.btn2.clicked.connect(self.threadStop)

        self.logger = QPlainTextEdit()
        self.logger.setReadOnly(True)
        vertBox.addWidget(self.logger)
 
        self.show()
 
        self.th = TestThread(self)
 
        self.th.threadEvent.connect(self.threadEventHandler)
 
    @pyqtSlot()
    def threadStart(self):
        if not self.th.isRun:
            self.th.isRun = True
            self.th.start()
 
    @pyqtSlot()
    def threadStop(self):
        if self.th.isRun:
            self.th.isRun = False
 
    @pyqtSlot(str)
    def threadEventHandler(self, n):
        print('main emit : %s' % n )
        self.logger.appendPlainText(n)
 
 
if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
    form = TestGUI()
    app.exec_()