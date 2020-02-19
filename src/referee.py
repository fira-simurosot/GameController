import sys
sys.path.insert(1, '../protoCompiled')

from protoCompiled.SIM2REF import packet_pb2
from src.firasimClient import FIRASimClient
from src.firasimServer import FIRASimServer
from src.common import WorldModel, GameState
from multiprocessing import Process
from PyQt5.QtWidgets import QApplication
from src.gameControllerWidget import GameControllerWidget

class Referee():
    def __init__(self):
        self.firasimserver = FIRASimServer('127.0.0.1', 50054)
        self.firasimclient = FIRASimClient('127.0.0.1', 50051)

        self.worldmodel = WorldModel()
        self.gamestate = GameState()
        self.app = None
        self.myWidget = None

        self.p = Process(target=self.firasimserver.start_receiveing, args=(self.vision_detection,))
        self.p.start()
        self.createGUI()


        # self.firasimserver.start_receiveing(self.vision_detection)

    def vision_detection(self, data):
        print(self.firasimclient)
        environment = packet_pb2.Environment()
        environment.ParseFromString(data)
        self.worldmodel.update_worldmodel(environment)

    def createGUI(self):
        self.app = QApplication(sys.argv)
        self.myWidget = GameControllerWidget()
        sys.exit(self.app.exec_())



if __name__ == "__main__":
    referee = Referee()
