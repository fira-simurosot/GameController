import sys
sys.path.insert(1, '../protoCompiled')

import socket
from protoCompiled.SIM2REF import packet_pb2
from src.common import WorldModel
from PyQt5.QtNetwork import QUdpSocket


class FIRASimServer():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.udpSocket = QUdpSocket()
        self.udpSocket.bind(self.port)
        self.udpSocket.readyRead.connect(self.handle_incoming)

    def set_function(self, function):
        self.vision_detection_function = function

    def handle_incoming(self):
        while self.udpSocket.hasPendingDatagrams():
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
        self.vision_detection_function(datagram)



if __name__ == "__main__":
    def func(data):
        enviroment = packet_pb2.Environment()
        enviroment.ParseFromString(data)
        worldmodel = WorldModel()
        worldmodel.update_worldmodel(enviroment)
    server = FIRASimServer('127.0.0.1', 50054)
    server.set_function(func)