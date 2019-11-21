#!/usr/bin/env python3

import os.path
import socket

SERVER_IP = "localhost"
SERVER_PORT = 4444
BUFFER_SIZE = 2048

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

def recvData(socket):
    data = socket.recv(BUFFER_SIZE)
    return data

print("Starting server") 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP, SERVER_PORT))
s.listen()
while True:
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(BUFFER_SIZE).decode()
            if not data:
                break
            print(data)
            if data == "PING":
                command = "UPDATE"
                conn.sendall(command.encode())
