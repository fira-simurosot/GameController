from enum import Enum
import time, math
from PyQt5.QtCore import QThread, pyqtSignal
from protoCompiled import common_pb2
from protoCompiled.REF2CLI import messages_pb2
from src.teamClient import TeamClient
from src.common import Converter


class WhatToCallEnum(Enum):
    Register = 1
    RunStrategy = 2
    SetBall = 3
    SetFormerRobots = 4
    SetLaterRobots = 5
    Nothing = 6


class ThreadClient(QThread):
    def __init__(self, ip, port, isYellow, firasimclient):
        super().__init__()

        self.teamClient = TeamClient(ip, port)
        self.converter = Converter()
        self.firasimclient = firasimclient


        self.isYellow = isYellow
        self.teamName = ''
        self.frame = common_pb2.Frame()
        self.foulinfo = messages_pb2.FoulInfo()
        self.what_to_call = WhatToCallEnum.Nothing


    def set_arguments(self, what_to_call, frame = common_pb2.Frame(), foulinfo = messages_pb2.FoulInfo()):
        self.frame = frame
        self.foulinfo = foulinfo
        self.what_to_call = what_to_call
        self.start()

    def run(self):
        if self.what_to_call == WhatToCallEnum.Nothing:
            pass
        elif self.what_to_call == WhatToCallEnum.Register:
            teaminfo = messages_pb2.TeamInfo()
            teaminfo.color = messages_pb2.Color.Y if self.isYellow else messages_pb2.Color.B
            res = self.teamClient.call_Register(teaminfo)
            self.teamName = res.name
        elif self.what_to_call == WhatToCallEnum.SetBall:
            res = self.teamClient.call_SetBall(self.frame, self.foulinfo)
            res = self.symmetric_ball_position(res) if self.isYellow else res
            ball = self.converter.convert_protoBall_to_Ball(res)
            self.firasimclient.send_ball_replacement(ball)
        elif self.what_to_call == WhatToCallEnum.SetFormerRobots:
            res = self.teamClient.call_SetFormerRobots(self.frame, self.foulinfo)
            res = self.symmetric_robot_position(res) if self.isYellow else res
            robots = self.converter.convert_protoRobots_to_Robot(res, self.isYellow)
            self.firasimclient.send_robot_replacement(robots)
            self.what_to_call = WhatToCallEnum.Nothing
        elif self.what_to_call == WhatToCallEnum.SetLaterRobots:
            res = self.teamClient.call_SetLaterRobots(self.frame, self.foulinfo)
            res = self.symmetric_robot_position(res) if self.isYellow else res
            robots = self.converter.convert_protoRobots_to_Robot(res, self.isYellow)
            self.firasimclient.send_robot_replacement(robots)
            self.what_to_call = WhatToCallEnum.Nothing
        elif self.what_to_call == WhatToCallEnum.RunStrategy:
            res = self.teamClient.call_RunStrategy(self.frame, self.foulinfo)
            command = self.converter.convert_protocommand_to_Robot(res, self.isYellow)
            self.firasimclient.send_robot_command(command)


    def symmetric_robot_position(self, protorobots):
        for robot in protorobots.robots:
            robot.x *= -1
            robot.orientation = math.pi - robot.orientation
        return protorobots

    def symmetric_ball_position(self, protoball):
        protoball.x *= -1
        return protoball


