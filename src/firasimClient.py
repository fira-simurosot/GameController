import sys
sys.path.insert(1, '../protoCompiled')

import socket
from protoCompiled import common_pb2
from protoCompiled.SIM2REF import packet_pb2, replacement_pb2, command_pb2
from protoCompiled.REF2CLI import messages_pb2
from src.common import Robot, Ball, Converter, ROBOT_NUM


class FIRASimClient():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        # sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


    def send_robot_command(self, robotsYellow = [], robotsBlue = []):
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
            robot_command.wheel_left = robot.wheel_left
            robot_command.wheel_right = robot.wheel_right

        packet = packet_pb2.Packet()
        packet.cmd.CopyFrom(commands)
        # print(packet)
        self.sock.sendto(packet.SerializeToString(), (self.ip, self.port))

    def send_halt_robot_command(self):
        yellow_robots = []
        blue_robots = []
        for i in range(ROBOT_NUM):
            yel = Robot()
            yel.id = i
            yel.isYellow = True
            yellow_robots.append(yel)
            blu = Robot()
            blu.id = i
            blu.isYellow = False
            blue_robots.append(blu)
        self.send_robot_command(yellow_robots, blue_robots)


    def send_robot_replacement(self, robotsYellow = [], robotsBlue = []):
        self.send_halt_robot_command()
        replacement = replacement_pb2.Replacement()
        for myrobot in robotsYellow:
            robot = replacement.robots.add()
            robot.position.robot_id = myrobot.id
            robot.position.x = myrobot.x
            robot.position.y = myrobot.y
            robot.position.orientation = myrobot.orientation
            robot.yellowteam = myrobot.isYellow
            robot.turnon = True
        for myrobot in robotsBlue:
            robot = replacement.robots.add()
            robot.position.robot_id = myrobot.id
            robot.position.x = myrobot.x
            robot.position.y = myrobot.y
            robot.position.orientation = myrobot.orientation
            robot.yellowteam = myrobot.isYellow
            robot.turnon = True

        packet = packet_pb2.Packet()
        packet.replace.CopyFrom(replacement)
        self.sock.sendto(packet.SerializeToString(), (self.ip, self.port))

    def send_ball_replacement(self, ball):
        self.send_halt_robot_command()
        replacement = replacement_pb2.Replacement()
        replacement.ball.x = ball.x
        replacement.ball.y = ball.y
        packet = packet_pb2.Packet()
        packet.replace.CopyFrom(replacement)
        self.sock.sendto(packet.SerializeToString(), (self.ip, self.port))





if __name__ == "__main__":
    cli = FIRASimClient('127.0.0.1', 50051)
    cli1 = FIRASimClient('127.0.0.1', 50051)

    conv = Converter()

    command = messages_pb2.Command()
    for i in range(5):
        wheelspeed = command.wheels.add()
        wheelspeed.robot_id = i
        wheelspeed.right = 10
        wheelspeed.left = -10
    yelbot = conv.convert_protocommand_to_Robot(command, True)
    blubot = conv.convert_protocommand_to_Robot(command, False)
    while True:
        cli.send_robot_command(robotsBlue=blubot)
        cli1.send_robot_command(robotsYellow=yelbot)


    # robots = messages_pb2.Robots()
    # for i in range(5):
    #     robot = robots.robots.add()
    #     robot.robot_id = i
    #     robot.x = 1
    #     robot.y = 1
    #     robot.orientation = 0
    # yelbot = conv.convert_protoRobots_to_Robot(robots, True)
    # blubot = conv.convert_protoRobots_to_Robot(robots, False)
    # while True:
    #     cli.send_robot_replacement(yelbot, blubot)

    # protoball = common_pb2.Ball()
    # protoball.x = 0.5
    # protoball.y = 0.5
    # ball = conv.convert_protoBall_to_Ball(protoball)
    # while True:
    #     cli.send_ball_replacement(ball)
