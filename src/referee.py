import sys
sys.path.insert(1, '../protoCompiled')

from protoCompiled.SIM2REF import packet_pb2
from protoCompiled import common_pb2
from protoCompiled.REF2CLI import messages_pb2, service_pb2_grpc, service_pb2
from src.firasimClient import FIRASimClient
from src.firasimServer import FIRASimServer
from src.common import WorldModel, GameState, GameStateEnum, ActorEnum, GamePhaseEnum, Converter
from multiprocessing import Process
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot, QTimer, QObject
from src.gameControllerWidget import GameControllerWidget
from src.teamClient import TeamClient

class Referee():
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.firasimserver = FIRASimServer('127.0.0.1', 50055)
        self.firasimclient = FIRASimClient('127.0.0.1', 50051)
        self.yellowClient = TeamClient('127.0.0.1', 50053)
        self.blueClient = TeamClient('127.0.0.1', 50052)

        self.firasimserver.set_function(self.vision_detection)
        self.worldmodel = WorldModel()
        self.gamestate = GameState()
        self.converter = Converter()
        self.gamecontrollerWidget = None

        self.createGUI()

        self.register_teams()
        sys.exit(self.app.exec_())



    def vision_detection(self, data):
        print(data)

        # environment = packet_pb2.Environment()
        # environment.ParseFromString(data)
        # # self.worldmodel.update_worldmodel(environment)
        # (foulinfo_yellow, foulinfo_blue) = self.generate_foulinfo()
        # (foulinfo_yellow, foulinfo_blue) = self.generate_foulinfo()



    def createGUI(self):
        self.gamecontrollerWidget = GameControllerWidget()
        self.gamecontrollerWidget.button_clicked.connect(self.button_listener)
        self.gamecontrollerWidget.widget_closed.connect(self.widget_closed)

    def widget_closed(self):
        pass

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
        elif buttonName == 'pbfirstHalf':
            self.gamestate.state = GameStateEnum.Stop
            self.gamestate.actor = ActorEnum.NoOne
            self.gamestate.phase = GamePhaseEnum.FirstHalf
            self.gamecontrollerWidget.start_timer(True)
        elif buttonName == 'pbsecondHalf':
            self.gamestate.state = GameStateEnum.Stop
            self.gamestate.actor = ActorEnum.NoOne
            self.gamestate.phase = GamePhaseEnum.SecondHalf
            self.gamecontrollerWidget.start_timer(True)
        elif buttonName == 'pbpenalty':
            self.gamestate.state = GameStateEnum.Stop
            self.gamestate.actor = ActorEnum.NoOne
            self.gamestate.phase = GamePhaseEnum.Penalty

    def generate_foulinfo(self):
        foulinfo_yellow = messages_pb2.FoulInfo()
        if self.gamestate.phase == GamePhaseEnum.FirstHalf:
            foulinfo_yellow.phase = messages_pb2.FoulInfo.PhaseType.FirstHalf
        elif self.gamestate.phase == GamePhaseEnum.SecondHalf:
            foulinfo_yellow.phase = messages_pb2.FoulInfo.PhaseType.SecondHalf
        elif self.gamestate.phase == GamePhaseEnum.Penalty:
            foulinfo_yellow.phase = messages_pb2.FoulInfo.PhaseType.PenaltyShootout
        elif self.gamestate.phase == GamePhaseEnum.Pause or self.gamestate.state == GameStateEnum.Stop:
            foulinfo_yellow.phase = messages_pb2.FoulInfo.PhaseType.Stopped

        if self.gamestate.state == GameStateEnum.PlayOn:
            foulinfo_yellow.type = messages_pb2.FoulInfo.FoulType.PlayOn
        elif self.gamestate.state == GameStateEnum.KickOff:
            foulinfo_yellow.type = messages_pb2.FoulInfo.FoulType.PlaceKick
        elif self.gamestate.state == GameStateEnum.Penalty:
            foulinfo_yellow.type = messages_pb2.FoulInfo.FoulType.PenaltyKick
        elif self.gamestate.state == GameStateEnum.FreeKick:
            foulinfo_yellow.type = messages_pb2.FoulInfo.FoulType.FreeKick
        elif self.gamestate.state == GameStateEnum.GoalKick:
            foulinfo_yellow.type = messages_pb2.FoulInfo.FoulType.GoalKick
        elif self.gamestate.state == GameStateEnum.FreeBallLeftTop:
            foulinfo_yellow.type = messages_pb2.FoulInfo.FoulType.FreeBallLeftTop
        elif self.gamestate.state == GameStateEnum.FreeBallRightTop:
            foulinfo_yellow.type = messages_pb2.FoulInfo.FoulType.FreeBallRightTop
        elif self.gamestate.state == GameStateEnum.FreeBallLeftBot:
            foulinfo_yellow.type = messages_pb2.FoulInfo.FoulType.FreeBallLeftBot
        elif self.gamestate.state == GameStateEnum.FreeBallRightBot:
            foulinfo_yellow.type = messages_pb2.FoulInfo.FoulType.FreeBallRightBot

        if self.gamestate.actor == ActorEnum.Yellow:
            foulinfo_yellow.actor = messages_pb2.Side.Self
        else:
            foulinfo_yellow.actor = messages_pb2.Side.Opponent

        foulinfo_blue = messages_pb2.FoulInfo()
        foulinfo_blue.CopyFrom(foulinfo_yellow)
        if self.gamestate.actor == ActorEnum.Yellow:
            foulinfo_blue.actor = messages_pb2.Side.Opponent
        else:
            foulinfo_yellow.actor = messages_pb2.Side.Self

        return (foulinfo_yellow, foulinfo_blue)

    def register_teams(self):
        frame = common_pb2.Frame()
        foulInfo = messages_pb2.FoulInfo()
        yellow_name = self.yellowClient.call_Register(frame, foulInfo)
        blue_name = self.blueClient.call_Register(frame, foulInfo)
        self.gamecontrollerWidget.set_teamnames(yellow_name.name, blue_name.name)

    def runStrategy_teams(self, frame, foulInfo):
        yellowCommand = self.yellowClient.call_RunStrategy(frame, foulInfo)
        BlueCommand = self.blueClient.call_RunStrategy(frame, foulInfo)
        yelbot = self.converter.convert_protocommand_to_Robot(yellowCommand, True)
        blubot = self.converter.convert_protocommand_to_Robot(BlueCommand, False)
        self.firasimclient.send_robot_command(yelbot, blubot)

    def robotPlacement_teams(self, frame, foulInfo):
        if self.gamestate.actor == ActorEnum.Yellow:
            yelbot = self.yellowClient.call_SetFormerRobots(frame, foulInfo)
            blubot = self.blueClient.call_SetLaterRobots(frame, foulInfo)
        else:
            blubot = self.blueClient.call_SetFormerRobots(frame, foulInfo)
            yelbot = self.yellowClient.call_SetLaterRobots(frame, foulInfo)
        yelbot = self.converter.convert_protoRobots_to_Robot(yelbot, True)
        blubot = self.converter.convert_protoRobots_to_Robot(blubot, False)
        self.firasimclient.send_robot_replacement(yelbot, blubot)

    def ballPlacement_teams(self, frame, foulInfo):
        if self.gamestate.actor == ActorEnum.Yellow:
            protoball = self.yellowClient.call_SetBall(frame, foulInfo)
        else:
            protoball = self.blueClient.call_SetBall(frame, foulInfo)
        ball = self.converter.convert_protoBall_to_Ball(protoball)
        self.firasimclient.send_ball_replacement(ball)


if __name__ == "__main__":
    referee = Referee()
