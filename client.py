import socket
import threading
import os
from time import sleep

BUFFERSIZE = 4096


def initConnection():
    HOST = '127.0.0.1'
    PORT = 5000

    try:
        s = socket.socket()
        s.connect((HOST, PORT))
        return s
    except socket.error, exc:
        # print "Caught exception socket.error : %s" % exc
        return None


def sendFile(filename, s):
    try:
        filesize = str(os.path.getsize(filename))

    except os.error:
        print("File not Found!")
        return None

    request = 'saveFile'
    s.send(request)  # Send Request
    serverResponse = s.recv(BUFFERSIZE)  # Primera Recepcion

    if serverResponse == 'OK':
        s.send(filename)  # Primer envio
        sleep(0.01)  # Tiene que ir!
        s.send(filesize)  # Segundo envio

        # print "SEND:",
        # print filename + " | ",
        # print filesize + " bytes."

        with open(filename, 'rb') as f:
            bytesToSend = f.read(1024)
            s.send(bytesToSend)
            while bytesToSend != "":
                bytesToSend = f.read(1024)
                s.send(bytesToSend)
        s.close()
        return 1
    else:
        print "Bad Request."
        return None


def Main():
    filename = "20171809-180001datos.txt"
    sock = initConnection()

    if sock is not None:
        status = sendFile(filename, sock)
        if status == 1:
            print "File " + filename + " sent!."
        else:
            print "Something went wrong !"
    else:
        print "Oops ... server unreachable ! "


if __name__ == '__main__':
    Main()
