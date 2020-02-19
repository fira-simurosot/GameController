import sys
sys.path.insert(1, '../protoCompiled')

from protoCompiled.SIM2REF import packet_pb2
from src.firasimClient import FIRASimClient
from src.firasimServer import FIRASimServer
from src.common import WorldModel, GameState
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
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.PlaceKick
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.B
        elif buttonName == 'pbPnaltyKickBlue':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.PenaltyKick
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.B
        elif buttonName == 'pbFreeKickBlue':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.FreeKick
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.B
        elif buttonName == 'pbGoalKickBlue':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.GoalKick
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.B
        elif buttonName == 'pbFreeBallLeftTopBlue':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.FreeBallLeftTop
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.B
        elif buttonName == 'pbFreeBallRightTopBlue':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.FreeBallRightTop
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.B
        elif buttonName == 'pbFreeBallLeftBotBlue':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.FreeBallLeftBot
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.B
        elif buttonName == 'pbFreeBallRightBotBlue':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.FreeBallRightBot
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.B

        elif buttonName == 'pbPlaceKickYellow':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.PlaceKick
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.Y
        elif buttonName == 'pbPnaltyKickYellow':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.PenaltyKick
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.Y
        elif buttonName == 'pbFreeKickYellow':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.FreeKick
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.Y
        elif buttonName == 'pbGoalKickYellow':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.GoalKick
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.Y
        elif buttonName == 'pbFreeBallLeftTopYellow':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.FreeBallLeftTop
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.Y
        elif buttonName == 'pbFreeBallRightTopYellow':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.FreeBallRightTop
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.Y
        elif buttonName == 'pbFreeBallLeftBotYellow':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.FreeBallLeftBot
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.Y
        elif buttonName == 'pbFreeBallRightBotYellow':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.FreeBallRightBot
            self.responseHandyRef.foulInfo.actorColor = messages_pb2.Color.Y

        elif buttonName == 'pbPlayOn':
            self.responseHandyRef.foulInfo.type = messages_pb2.FoulInfo.FoulType.PlayOn
        elif buttonName == 'pbStop':
            self.responseHandyRef.foulInfo.phase = messages_pb2.FoulInfo.PhaseType.Stopped
        #TODO referee dowsnt provide halt we act like stop for now
        elif buttonName == 'pbHalt':
            self.responseHandyRef.foulInfo.phase = messages_pb2.FoulInfo.PhaseType.Stopped



if __name__ == "__main__":
    referee = Referee()
