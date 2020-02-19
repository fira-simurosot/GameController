import sys
sys.path.insert(1, '../protoCompiled')

from protoCompiled.SIM2REF import packet_pb2
from protoCompiled import common_pb2
from protoCompiled.REF2CLI import messages_pb2, service_pb2_grpc, service_pb2
from src.firasimClient import FIRASimClient
from src.firasimServer import FIRASimServer
from src.common import WorldModel, GameState, GameStateEnum, ActorEnum
from multiprocessing import Process
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot
from src.gameControllerWidget import GameControllerWidget
from src.teamClient import TeamClient

class Referee():
    def __init__(self):
        self.firasimserver = FIRASimServer('127.0.0.1', 50055)
        self.firasimclient = FIRASimClient('127.0.0.1', 50051)
        self.yellowClient = TeamClient('127.0.0.1', 50053)
        self.blueClient = TeamClient('127.0.0.1', 50052)


        self.worldmodel = WorldModel()
        self.gamestate = GameState()
        self.app = None
        self.gamecontrollerWidget = None


        self.p = Process(target=self.firasimserver.start_receiveing, args=(self.vision_detection,))
        self.p.start()
        self.createGUI()
        self.register_teams()
        sys.exit(self.app.exec_())



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

    def register_teams(self):
        frame = common_pb2.Frame()
        foulInfo = messages_pb2.FoulInfo()
        yellow_name = self.yellowClient.call_Register(frame, foulInfo)
        if yellow_name == None:
            yellow_name = 'not registered'
        else:
            yellow_name = yellow_name.name
        blue_name = self.blueClient.call_Register(frame, foulInfo)
        if blue_name == None:
            blue_name = 'not registered'
        else:
            blue_name = blue_name.name
        self.gamecontrollerWidget.set_teamnames(yellow_name, blue_name)

if __name__ == "__main__":
    referee = Referee()
