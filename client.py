#!/usr/bin/env python3

import os.path
import socket
from datetime import datetime
import time
import random
import uuid
from platform import node

SERVER_IP = "localhost"
SERVER_PORT = 4444
BUFFER_SIZE = 2048
DEATH_DATE = datetime(2020,1,20)
OS = os.popen("lsb_release -d | cut -d ':' -f2").read().strip()
UUID = uuid.uuid1()
HOSTNAME = node().strip()

def connectToServer(ip, port):
    print("Connecting to server")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s

def sendData(socket, data):
    print("Sending Data")
    socket.sendall(data.encode())

def closeSocket(socket):
    print("Closing Socket")
    socket.close()

if __name__ == "__main__":
    print("Starting client")
    while datetime.now() < DEATH_DATE:
        s = connectToServer(SERVER_IP, SERVER_PORT)
        sendData(s, "PING")
        print("Recieving data")
        data = s.recv(BUFFER_SIZE).decode()
        if data:
            print(data)
            if data == "UPDATE":
                info = "UPDATE RESPONSE\r\n"
                info += str(UUID) + "\r\n"
                info += OS + "\r\n"
                info += HOSTNAME + "\r\n"
                sendData(s, info)
        closeSocket(s)
        time.sleep(random.randint(1,10))
