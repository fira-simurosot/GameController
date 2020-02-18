import sys
sys.path.insert(1, '../protoCompiled')

import socket
from protoCompiled.SIM2REF import packet_pb2
from src.common import WorldModel

class FIRASimServer():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.bind((self.ip, self.port))

    def start_receiveing(self, function):
        while True:
            data, addr = self.sock.recvfrom(1024)
            function(data)


if __name__ == "__main__":
    def func(data):
        enviroment = packet_pb2.Environment()
        enviroment.ParseFromString(data)
        worldmodel = WorldModel()
        worldmodel.update_worldmodel(enviroment)
    server = FIRASimServer('127.0.0.1', 50054)
    server.start_receiveing(func)