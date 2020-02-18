import sys
sys.path.insert(1, '../protoCompiled')

import socket
from protoCompiled import common_pb2
from protoCompiled.SIM2REF import packet_pb2, replacement_pb2, command_pb2
from protoCompiled.REF2CLI import messages_pb2
from src.common import Robot, Ball


class FIRASimClient():
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 50051

        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        # sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


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

    def send_robot_command(self, robotsYellow, robotsBlue):
        commands = command_pb2.Commands()
        for robot in robotsYellow:
            robot_command = commands.robot_commands.add()
            robot_command.id = robot.id
            robot_command.yellowteam = robot.isYellow
            robot_command.wheel_left = robot.wheel_left
            robot_command.wheel_right = robot.wheel_right
        for robot in robotsBlue:
            robot_command = commands.robot_commands.add()
            robot_command.id = robot.id
            robot_command.yellowteam = robot.isYellow
            print(robot_command.yellowteam)
            robot_command.wheel_left = robot.wheel_left
            robot_command.wheel_right = robot.wheel_right

        packet = packet_pb2.Packet()
        packet.cmd.CopyFrom(commands)
        # print(packet)
        self.sock.sendto(packet.SerializeToString(), (self.ip, self.port))

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

    def send_robot_replacement(self, robotsYellow, robotsBlue):
        replacement = replacement_pb2.Replacement()
        for myrobot in robotsYellow:
            robot = replacement.robots.add()
            robot.position.robot_id = myrobot.id
            robot.position.x = myrobot.x
            robot.position.y = myrobot.y
            robot.position.orientation = myrobot.orientation
            robot.yellowteam = True
            robot.turnon = True

        for myrobot in robotsBlue:
            robot = replacement.robots.add()
            robot.position.robot_id = myrobot.id
            robot.position.x = myrobot.x
            robot.position.y = myrobot.y
            robot.position.orientation = myrobot.orientation
            robot.yellowteam = False
            robot.turnon = True

        packet = packet_pb2.Packet()
        packet.replace.CopyFrom(replacement)
        self.sock.sendto(packet.SerializeToString(), (self.ip, self.port))

    def convert_protoBall_to_Ball(self, protoball):
        ball = Ball()
        ball.x = protoball.x
        ball.y = protoball.y
        ball.z = protoball.z
        return ball

    def send_ball_replacement(self, ball):
        replacement = replacement_pb2.Replacement()
        replacement.ball.x = ball.x
        replacement.ball.y = ball.y
        packet = packet_pb2.Packet()
        packet.replace.CopyFrom(replacement)
        self.sock.sendto(packet.SerializeToString(), (self.ip, self.port))





if __name__ == "__main__":
    cli = FIRASimClient()

    # command = messages_pb2.Command()
    # for i in range(5):
    #     wheelspeed = command.wheels.add()
    #     wheelspeed.robot_id = i
    #     wheelspeed.right = 10
    #     wheelspeed.left = -10
    # yelbot = cli.convert_protocommand_to_Robot(command, True)
    # blubot = cli.convert_protocommand_to_Robot(command, False)
    #
    # while True:
    #     cli.send_robot_command(yelbot, blubot)

    # robots = messages_pb2.Robots()
    # for i in range(5):
    #     robot = robots.robots.add()
    #     robot.robot_id = i
    #     robot.x = 1
    #     robot.y = 1
    #     robot.orientation = 0
    # yelbot = cli.convert_protoRobots_to_Robot(robots, True)
    # blubot = cli.convert_protoRobots_to_Robot(robots, False)
    # while True:
    #     cli.send_robot_replacement(yelbot, blubot)

    protoball = common_pb2.Ball()
    protoball.x = 0.5
    protoball.y = 0.5
    ball = cli.convert_protoBall_to_Ball(protoball)
    while True:
        cli.send_ball_replacement(ball)
