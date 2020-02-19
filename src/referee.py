import sys
sys.path.insert(1, '../protoCompiled')

from protoCompiled.SIM2REF import packet_pb2
from src.firasimClient import FIRASimClient
from src.firasimServer import FIRASimServer
from src.common import WorldModel, GameState


class Referee():
    def __init__(self):
        self.firasimserver = FIRASimServer('127.0.0.1', 50054)
        self.firasimclient = FIRASimClient('127.0.0.1', 50051)

        self.worldmodel = WorldModel()
        self.gamestate = GameState()

        self.firasimserver.start_receiveing(self.vision_detection)

    def vision_detection(self, data):
        environment = packet_pb2.Environment()
        environment.ParseFromString(data)
        self.worldmodel.update_worldmodel(environment)



if __name__ == "__main__":
    referee = Referee()