#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

def getFileSize(fileName):
    size = os.stat(fileName)
    if size.st_size > 100:
        print("Error... The file exceed the 100 bytes")
        cmd()
    return size.st_size

def readFile(fileName):

    #checking if the text file exist
    if not os.path.exists(fileName):
        print ("text file input %s doesn't exist!" % fileName)
        cmd()
        # exit()

    readFile = open(fileName,"r")
    print("reading File...")
    fileData2 = readFile.read()
    readFile.close()
    fileData1 = fileName
    fileData1 += ":"+fileData2
    file = bytearray(fileData1, 'utf-8')
    return file.rstrip()

def cmd():
    command=input(">>$ ")
    while(command !="q"):
        if ("put" in command):
            fileData= command.split(" ")
            fileName= fileData[1]
            data=readFile(fileName).rstrip()
            size=getFileSize(fileName)
            print("encoding file...")
            # print(data)
            framedSend(s, data, debug)
            print("received:", framedReceive(s, debug),"\n")
        command=input(">>$ ")

if usage:
    params.usage()
try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print("attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)


print("connection established!")
cmd()
