import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QPushButton, QApplication, QLabel, QComboBox, QLineEdit, QSizePolicy)
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import QTimer, pyqtSignal
from functools import partial



class GameControllerWidget(QWidget):
    button_clicked = pyqtSignal(['QString'])
    widget_closed = pyqtSignal()
    def __init__(self):
        super(GameControllerWidget, self).__init__()

        self.timer = QTimer()
        self.min = 0
        self.sec = 0

        self.step = 0

        self.createWidget()
        self.connections()

    def createWidget(self):
        uic.loadUi('../resources/gcWidget.ui', self) # Load the .ui file
        self.show()


    def connections(self):
        self.timer.timeout.connect(self.handleTimer)

        self.pbPlaceKickBlue.clicked.connect(partial(self.btnListener, "pbPlaceKickBlue"))
        self.pbPnaltyKickBlue.clicked.connect(partial(self.btnListener, "pbPnaltyKickBlue"))
        self.pbFreeKickBlue.clicked.connect(partial(self.btnListener, "pbFreeKickBlue"))
        self.pbGoalKickBlue.clicked.connect(partial(self.btnListener, "pbGoalKickBlue"))
        self.pbFreeBallLeftTopBlue.clicked.connect(partial(self.btnListener, "pbFreeBallLeftTopBlue"))
        self.pbFreeBallRightTopBlue.clicked.connect(partial(self.btnListener, "pbFreeBallRightTopBlue"))
        self.pbFreeBallLeftBotBlue.clicked.connect(partial(self.btnListener, "pbFreeBallLeftBotBlue"))
        self.pbFreeBallRightBotBlue.clicked.connect(partial(self.btnListener, "pbFreeBallRightBotBlue"))

        self.pbPlaceKickYellow.clicked.connect(partial(self.btnListener, "pbPlaceKickYellow"))
        self.pbPnaltyKickYellow.clicked.connect(partial(self.btnListener, "pbPnaltyKickYellow"))
        self.pbFreeKickYellow.clicked.connect(partial(self.btnListener, "pbFreeKickYellow"))
        self.pbGoalKickYellow.clicked.connect(partial(self.btnListener, "pbGoalKickYellow"))
        self.pbFreeBallLeftTopYellow.clicked.connect(partial(self.btnListener, "pbFreeBallLeftTopYellow"))
        self.pbFreeBallRightTopYellow.clicked.connect(partial(self.btnListener, "pbFreeBallRightTopYellow"))
        self.pbFreeBallLeftBotYellow.clicked.connect(partial(self.btnListener, "pbFreeBallLeftBotYellow"))
        self.pbFreeBallRightBotYellow.clicked.connect(partial(self.btnListener, "pbFreeBallRightBotYellow"))

        self.pbPlayOn.clicked.connect(partial(self.btnListener, "pbPlayOn"))
        self.pbStop.clicked.connect(partial(self.btnListener, "pbStop"))
        self.pbHalt.clicked.connect(partial(self.btnListener, "pbHalt"))


    def btnListener(self, buttonName):
        self.button_clicked.emit(buttonName)

    def set_teamnames(self, yellow_name, blue_name):
        self.labelTeamNameYellow.setText(yellow_name)
        self.labelTeamNameBlue.setText(blue_name)

    def startTimer(self):
        self.timer.start(1000)

    def handleTimer(self):
        self.sec += 1
        if self.sec == 60:
            self.min += 1
            self.sec = 0
        self.labelTimer.setText(str(self.min) + ':' + str(self.sec))

    def updateStats(self, scoreBlue, scoreYellow):
        #handle request
        self.step += 1
        self.labelsteper.setText('step ' + str(self.step) + ' / 18000')
        self.labelScoreBlue.setText(str(scoreBlue))
        self.labelScoreYellow.setText(str(scoreYellow))

        #create response
        tmp = messages_pb2.HandyRef()
        tmp.CopyFrom(self.responseHandyRef)
        if self.checkIgnore.isChecked():
            tmp.isOwerWriting = True
        self.responseHandyRef.Clear()
        return tmp

    def closeEvent(self, event):
        self.widget_closed.emit()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameControllerWidget()
    sys.exit(app.exec_())

