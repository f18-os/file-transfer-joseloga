#! /usr/bin/env python3
import sys
sys.path.append("../lib")       # for params

import os, re, socket, params


switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
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

def writeToFile(filename, data):
    mkdir('./Received/')
    currentdir=os.getcwd()+"/"
    dir=os.getcwd()+"/Received/"
    fileExists = os.path.isfile(dir+filename)
    if fileExists:
        print ("file exists")
        framedSend(sock, b'file already exist!', debug)
    else:
        # create file
        file = open(dir+filename, "wb+") # open for [w]riting as [b]inary
        print(data,"data..........")
        file.write(data)
        file.close()
        # os.rename(currentdir+values,dir+values)

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        filename=""
        while True:
            payload = framedReceive(sock, debug)
            print(payload,"-----------------")
            payload2 = framedReceive(sock, debug)
            print(payload2,"+++++++++++++++++++++")

            char="/n"
            decode =bytearray(char,'utf-8')
            if decode in payload:
                filename= payload.decode("utf-8")
                filename= filename[:-2]
                print("file name: ",filename)
        # ?        payload = framedReceive(sock, debug)
                print(payload2)
                writeToFile(filename,payload2)

            if debug: print("rec'd: ", payload)

            if not payload:
                if debug: print("child exiting")
                sys.exit(0)
            # payload += b"!"             # make emphatic!
            framedSend(sock, b'file trasfered!', debug)
