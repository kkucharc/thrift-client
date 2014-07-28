import json
from random import randint

# Zczytywanie konfiguracji z pliku json i zeracanie parmetrow 
# losowo wybranego serwera do ktorego nalezy sie polaczyc.

#TODO reconnection
class Server:
    servers = ''
    firstchoice = -1
    recentchoice = -1
    amount = -1
    def  __init__(self):
        self.servers = self.openConfig()
        
    def parseConfig(self):
        for i in self.servers:
            print i

    def getServer(self):
        self.amount =  len(self.servers)
        if self.amount != 0:
            self.firstchoice = self.recentchoice = randint(0,self.amount-1)
            socket = self.servers[self.recentchoice]
            return socket
        else:
            return 0
        
    def nextServer(self):
        self.recentchoice = (self.recentchoice + 1) % self.amount
        if self.recentchoice != self.firstchoice:
            return self.servers[self.recentchoice]
        else: 
            return 0
        
    def openConfig(self):
        try:
            config_json = open('config.json')
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Sprobuj jeszcze raz"
            return 
        file = json.load(config_json)
        config_json.close()
        return file['servers']