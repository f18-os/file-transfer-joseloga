#! /usr/bin/env python3
import sys
sys.path.append("../lib")       # for params
import os, re, socket, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", True), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

def mkdir(folderName):
    try:
        if not os.path.exists(folderName):
            os.makedirs(folderName)
    except OSError:
        pass

def writeToFile(values):
    mkdir('./Received/')
    currentdir=os.getcwd()+"/"
    dir=os.getcwd()+"/Received/"
    # create new file
    f=open(values[0],"w+")
    # f=open("received.txt","wb")
    f.write(values[1])
    os.rename(currentdir+values[0],dir+values[0])


if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

sock, addr = lsock.accept()
print("connection rec'd from", addr)

from framedSock import framedSend, framedReceive

while True:
    # print('Server received', repr(data))
    payload = framedReceive(sock, debug)

    if payload:
        # print(payload,"-------------------------")
        values = payload.decode('utf-8').split(':')
        print(values)
        writeToFile(values)

    if debug: print("rec'd: ", payload)
    if not payload:
        break
    payload += b"!"             # make emphatic!
    framedSend(sock, payload, debug)
