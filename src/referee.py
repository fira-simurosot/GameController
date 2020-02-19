import sys
sys.path.insert(1, '../protoCompiled')

from protoCompiled.SIM2REF import packet_pb2
from src.firasimClient import FIRASimClient
from src.firasimServer import FIRASimServer
from src.common import WorldModel, GameState, GameStateEnum, ActorEnum
from multiprocessing import Process
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot
from src.gameControllerWidget import GameControllerWidget

class Referee():
    def __init__(self):
        self.firasimserver = FIRASimServer('127.0.0.1', 50055)
        self.firasimclient = FIRASimClient('127.0.0.1', 50051)

        self.worldmodel = WorldModel()
        self.gamestate = GameState()
        self.app = None
        self.gamecontrollerWidget = None

        self.p = Process(target=self.firasimserver.start_receiveing, args=(self.vision_detection,))
        self.p.start()
        self.createGUI()

    def vision_detection(self, data):
        # print(data)
        environment = packet_pb2.Environment()
        environment.ParseFromString(data)
        self.worldmodel.update_worldmodel(environment)

    def createGUI(self):
        self.app = QApplication(sys.argv)
        self.gamecontrollerWidget = GameControllerWidget()
        self.gamecontrollerWidget.button_clicked.connect(self.button_listener)
        self.gamecontrollerWidget.widget_closed.connect(self.widget_closed)
        sys.exit(self.app.exec_())

    def widget_closed(self):
        self.p.kill()

    def button_listener(self, buttonName):
        if buttonName == 'pbPlaceKickBlue':
            self.gamestate.state = GameStateEnum.KickOff
            self.gamestate.actor = ActorEnum.Blue
        elif buttonName == 'pbPnaltyKickBlue':
            self.gamestate.state = GameStateEnum.Penalty
            self.gamestate.actor = ActorEnum.Blue
        elif buttonName == 'pbFreeKickBlue':
            self.gamestate.state = GameStateEnum.FreeKick
            self.gamestate.actor = ActorEnum.Blue
        elif buttonName == 'pbGoalKickBlue':
            self.gamestate.state = GameStateEnum.GoalKick
            self.gamestate.actor = ActorEnum.Blue
        elif buttonName == 'pbFreeBallLeftTopBlue':
            self.gamestate.state = GameStateEnum.FreeBallLeftTop
            self.gamestate.actor = ActorEnum.Blue
        elif buttonName == 'pbFreeBallRightTopBlue':
            self.gamestate.state = GameStateEnum.FreeBallRightTop
            self.gamestate.actor = ActorEnum.Blue
        elif buttonName == 'pbFreeBallLeftBotBlue':
            self.gamestate.state = GameStateEnum.FreeBallLeftBot
            self.gamestate.actor = ActorEnum.Blue
        elif buttonName == 'pbFreeBallRightBotBlue':
            self.gamestate.state = GameStateEnum.FreeBallRightBot
            self.gamestate.actor = ActorEnum.Blue

        elif buttonName == 'pbPlaceKickYellow':
            self.gamestate.state = GameStateEnum.KickOff
            self.gamestate.actor = ActorEnum.Yellow
        elif buttonName == 'pbPnaltyKickYellow':
            self.gamestate.state = GameStateEnum.Penalty
            self.gamestate.actor = ActorEnum.Yellow
        elif buttonName == 'pbFreeKickYellow':
            self.gamestate.state = GameStateEnum.FreeKick
            self.gamestate.actor = ActorEnum.Yellow
        elif buttonName == 'pbGoalKickYellow':
            self.gamestate.state = GameStateEnum.GoalKick
            self.gamestate.actor = ActorEnum.Yellow
        elif buttonName == 'pbFreeBallLeftTopYellow':
            self.gamestate.state = GameStateEnum.FreeBallLeftTop
            self.gamestate.actor = ActorEnum.Yellow
        elif buttonName == 'pbFreeBallRightTopYellow':
            self.gamestate.state = GameStateEnum.FreeBallRightTop
            self.gamestate.actor = ActorEnum.Yellow
        elif buttonName == 'pbFreeBallLeftBotYellow':
            self.gamestate.state = GameStateEnum.FreeBallLeftBot
            self.gamestate.actor = ActorEnum.Yellow
        elif buttonName == 'pbFreeBallRightBotYellow':
            self.gamestate.state = GameStateEnum.FreeBallRightBot
            self.gamestate.actor = ActorEnum.Yellow

        elif buttonName == 'pbPlayOn':
            self.gamestate.state = GameStateEnum.PlayOn
            self.gamestate.actor = ActorEnum.NoOne
        elif buttonName == 'pbStop':
            self.gamestate.state = GameStateEnum.Stop
            self.gamestate.actor = ActorEnum.NoOne
        elif buttonName == 'pbHalt':
            self.gamestate.state = GameStateEnum.Halt
            self.gamestate.actor = ActorEnum.NoOne



if __name__ == "__main__":
    referee = Referee()
