import socket
import threading
from time import sleep
import os
import sys

HOST = '127.0.0.1'
PORT = 5000
BUFFERSIZE = 4096
WORKING_PATH = os.getcwd()

def decodeFileName(name):
    date, hour = name.split('-')
    return date

def createFolder(path, folderName):
    os.chdir(path)
    if not os.path.isdir(folderName):
        os.makedirs(folderName)
        print "Folder '" + folderName + "' created."
    else:
        print "Folder '" + folderName + "' already in current path."

def saveFile(name, sock, path):
    filename = sock.recv(BUFFERSIZE)  # Primera Recepcion
    filesize = sock.recv(BUFFERSIZE)  # Segunda Recepcion
    print "Incoming: ",
    print filename + " | ",
    print filesize + " bytes."

    date = decodeFileName(filename)
    createFolder(path, date)
    os.chdir(path + "\\" + date)

    f = open(filename, 'wb')

    data = sock.recv(BUFFERSIZE)
    totalrecv = len(data)
    f.write(data)

    while totalrecv < long(filesize):
        data = sock.recv(BUFFERSIZE)
        totalrecv += len(data)
        f.write(data)
        #print "{0:.2f}".format((totalrecv / float(filesize)) * 100) + "% Done"

    print "File Saved!\n"
    os.chdir(path)
    f.close()
    sock.close()


# Print files in folder
def listFiles(startpath):
    print("Files in: " + startpath)
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def handler(name, sock):
    request = sock.recv(BUFFERSIZE)  # Primera Recepcion

    if request == 'saveFile':
        print "Client Request: saveFiles"
        sock.send('OK')  # Send Confirmation
        saveFile(name, sock, WORKING_PATH + "\Data")

    elif request == 'listFiles':
        print "Internal Request: listFiles"
        sock.send('OK')  # Send Confirmation
        listFiles(WORKING_PATH + "\Data")

    else:
        sock.send('INVALID')  # Send Confirmation
        print "Request: not found"


def Main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)     #5 connections
    print "Server Started.\n"

    while True:
        c, addr = s.accept()
        #print "client connected ip:<" + str(addr) + ">"
        t = threading.Thread(target=handler, args=("RetrThread", c))
        t.start()

    s.close()


if __name__ == '__main__':
    Main()
