from protoCompiled import common_pb2
from protoCompiled.SIM2REF import packet_pb2, replacement_pb2, command_pb2
from protoCompiled.REF2CLI import messages_pb2
from enum import Enum

class Robot():
    def __init__(self):
        self.id = 0
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.isYellow = True
        self.wheel_right = 0.0
        self.wheel_left = 0.0

class Ball():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

class WorldModel():
    def __init__(self):
        self.ball = Ball()
        self.yellows = []
        self.blues = []
        for i in range(5):
            yel = Robot()
            yel.id = i
            yel.isYellow = True
            self.yellows.append(yel)
            blu = Robot()
            blu.id = i
            blu.isYellow = False
            blu.isYellow = False
            self.blues.append(blu)

    def update_worldmodel(self, enviroment):
        self.ball.x = enviroment.frame.ball.x
        self.ball.y = enviroment.frame.ball.y
        self.ball.z = enviroment.frame.ball.z

        for i in range(len(enviroment.frame.robots_yellow)):
            self.blues[i].id = enviroment.frame.robots_yellow[i].robot_id
            self.blues[i].x = enviroment.frame.robots_yellow[i].x
            self.blues[i].y = enviroment.frame.robots_yellow[i].y
            self.blues[i].orientation = enviroment.frame.robots_yellow[i].orientation
        for i in range(len(enviroment.frame.robots_blue)):
            self.blues[i].id = enviroment.frame.robots_blue[i].robot_id
            self.blues[i].x = enviroment.frame.robots_blue[i].x
            self.blues[i].y = enviroment.frame.robots_blue[i].y
            self.blues[i].orientation = enviroment.frame.robots_blue[i].orientation


class ActorEnum(Enum):
    Yellow = 1
    Blue = 2
    NoOne = 3


class GameState():
    def __init__(self):
        self.state = messages_pb2.FoulInfo.FoulType.PlaceKick
        self.actor = ActorEnum.NoOne
        self.phase = messages_pb2.FoulInfo.PhaseType.FirstHalf

    def need_robot_placement(self):
        return self.state != messages_pb2.FoulInfo.FoulType.PlayOn

    def need_ball_placement(self):
        return self.state == messages_pb2.FoulInfo.FoulType.GoalKick

    def is_play_on(self):
        return self.state == messages_pb2.FoulInfo.FoulType.PlayOn

class Converter():
    def __init__(self):
        pass

    def convert_protocommand_to_Robot(self, command, isYellow):
        robots = []
        for robot in command.wheels:
            robottmp = Robot()
            robottmp.id = robot.robot_id
            robottmp.isYellow = isYellow
            robottmp.wheel_left = robot.left
            robottmp.wheel_right = robot.right
            robots.append(robottmp)
        return robots

    def convert_protoRobots_to_Robot(self, protoRobots, isYellow):
        robots = []
        for robot in protoRobots.robots:
            robottmp = Robot()
            robottmp.id = robot.robot_id
            robottmp.isYellow = isYellow
            robottmp.x = robot.x
            robottmp.y = robot.y
            robottmp.orientation = robot.orientation
            robots.append(robottmp)
        return robots

    def convert_protoBall_to_Ball(self, protoball):
        ball = Ball()
        ball.x = protoball.x
        ball.y = protoball.y
        ball.z = protoball.z
        return ball

