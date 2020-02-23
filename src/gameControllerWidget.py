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

        self.pbTeamNameYellow.clicked.connect(partial(self.btnListener, "pbTeamNameYellow"))
        self.pbTeamNameBlue.clicked.connect(partial(self.btnListener, "pbTeamNameBlue"))

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
        self.pbfirstHalf.clicked.connect(partial(self.btnListener, "pbfirstHalf"))
        self.pbsecondHalf.clicked.connect(partial(self.btnListener, "pbsecondHalf"))
        self.pbpenalty.clicked.connect(partial(self.btnListener, "pbpenalty"))

    def btnListener(self, buttonName):
        self.button_clicked.emit(buttonName)
        if buttonName == 'pbfirstHalf':
            self.start_timer(True)
            self.step = 0
        elif buttonName == 'pbsecondHalf':
            self.start_timer(True)
            self.step = 0
        elif buttonName == 'pbpenalty':
            self.start_timer(True)
            self.step = 0
        elif buttonName == 'pbpenalty':
            self.start_timer(True)
            self.step = 0
        elif buttonName == 'pbTeamNameYellow':
            self.labelScoreYellow.setText(str(int(self.labelScoreYellow.text()) + 1))
        elif buttonName == 'pbTeamNameBlue':
            self.labelScoreBlue.setText(str(int(self.labelScoreBlue.text()) + 1))

    def set_teamnames(self, yellow_name, blue_name):
        self.pbTeamNameYellow.setText(yellow_name)
        self.pbTeamNameBlue.setText(blue_name)

    def start_timer(self, clean):
        if clean:
            self.min = 0
            self.sec = 0
            self.step = 0
        self.timer.start(1000)

    def handleTimer(self):
        self.sec += 1
        if self.sec == 60:
            self.min += 1
            self.sec = 0
        self.labelTimer.setText(str(self.min) + ':' + str(self.sec))

    def stepper(self):
        self.step += 1
        self.labelsteper.setText('step ' + str(self.step) + ' / 18000')
        if self.step > 18000:
            self.labelsteper.setStyleSheet('QLabel{color: red}')

    def updateScores(self, scoreBlue, scoreYellow):
        self.labelScoreBlue.setText(str(scoreBlue))
        self.labelScoreYellow.setText(str(scoreYellow))

    def closeEvent(self, event):
        self.widget_closed.emit()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameControllerWidget()
    sys.exit(app.exec_())

