import sys
sys.path.insert(1, '../protoCompiled')

import grpc
from protoCompiled.REF2CLI import messages_pb2, service_pb2, service_pb2_grpc
from protoCompiled import common_pb2

class TeamClient():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.channel = grpc.insecure_channel(self.ip + ':' + str(self.port))
        self.stub = service_pb2_grpc.RefereeStub(self.channel)

    def create_environment(self, frame, foulInfo):
        environment = messages_pb2.Environment()
        environment.frame.CopyFrom(frame)
        environment.foulInfo.CopyFrom(foulInfo)
        return environment

    def call_Register(self, frame, foulInfo):
        environment = self.create_environment(frame, foulInfo)
        try:
            response = self.stub.Register(environment)
        except:
            response = messages_pb2.TeamName()
        return response

    def call_RunStrategy(self, frame, foulInfo):
        environment = self.create_environment(frame, foulInfo)
        try:
            response = self.stub.RunStrategy(environment)
        except:
            response = messages_pb2.Command()
        return response

    def call_SetBall(self, frame, foulInfo):
        environment = self.create_environment(frame, foulInfo)
        try:
            response = self.stub.SetBall(environment)
        except:
            response = common_pb2.Ball()
        return response

    def call_SetFormerRobots(self, frame, foulInfo):
        environment = self.create_environment(frame, foulInfo)
        try:
            response = self.stub.SetFormerRobots(environment)
        except:
            response = messages_pb2.Robots()
        return response

    def call_SetLaterRobots(self, frame, foulInfo):
        environment = self.create_environment(frame, foulInfo)
        try:
            response = self.stub.SetLaterRobots(environment)
        except:
            response = messages_pb2.Robots()
        return response





if __name__ == "__main__":
    teamClient = TeamClient('127.0.0.1', 50052)
    frame = common_pb2.Frame()
    foulInfo = messages_pb2.FoulInfo()
    print(teamClient.call_Register(frame, foulInfo))