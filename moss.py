#!/usr/bin/python

import requests
import socket
import sys
import os

SERVER = "moss.stanford.edu"
PORT = 7690

class moss:
    def __init__(self, userid):
        self.server = "moss.stanford.edu"
        self.port = 7690
        self.userid = userid

    def connect(self):
        directory = 1
        lang = "javascript"
        optm = 10
        optx = 0
        self.optc = ""
        optn = 250
        bindex = 0


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((SERVER, PORT))

        self.sock.send("moss %s\n" %self.userid)
        self.sock.send("directory %d\n" %directory)
        self.sock.send("X %d\n" %optx)
        self.sock.send("maxmatches %d\n" %optm)
        self.sock.send("show %d\n" %optn)

        self.sock.send("language %s\n" %lang )
        response = self.sock.recv(1024)

        if response=="no":
            self.sock.send("end\n")
            print("Unsupported language")
            exit()

    def sendfile(self, filename, path, project, fileid, lang):
        with open(path, 'r') as fd:
            content = fd.read()
        size = len(content)

        print("uploading %s" %filename)

        self.sock.send("file %d %s %d %s\n" %(fileid, lang, size, os.path.join(project, filename)))
        self.sock.send(content)

    def finish(self):
        self.sock.send("query 0 %s\n" %self.optc)
        response = self.sock.recv(2048)
        print(response)
        self.sock.send("end\n")
        self.sock.close()

