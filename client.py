#!/usr/bin/env python
 
import sys, os

from clientconnection import ClientConnection
from thrift import Thrift
from thrift.transport import TTransport
from services.ttypes import *
from services.constants import *

# Menu glowne i operacje

class Menu:
    resources = []
    clientconn = ''
    def __init__(self):
        self.resources = sys.argv
        self.clientconn = ClientConnection()
      
     #TODO walidacja
    def choice(self):
        if len(self.resources) == 1:
            print "Nie wybrano operacji"
            return
        selection = self.resources[1]
        choice = self.resources[2:]
        if selection =='add':
            if len(choice) == 2:
                self.addFile(choice)
            else:
                print "Za malo parametrow"
                return
        elif selection == 'get':
            if len(choice) == 0:
                print "Brak parametrow operacji"
                return
            self.getFile(choice)
        elif selection == 'rm':
            if len(choice) == 0:
                print "Brak parametrow operacji"
                return
            self.rmFile(choice)
        elif selection == 'mv':
            if len(choice) == 0:
                print "Brak parametrow operacji"
                return
            self.mvFile(choice)
        elif selection == 'ls':
            if len(choice) == 0:
                print "Brak parametrow operacji"
                return
            self.lsDir(choice)
        elif selection == 'help':
            print "Amazing file repo\n Uzywanie:\n"\
            "-- ./client.py add <lokalizacja docelowa> <plik>\n"\
            "-- ./client.py get <lokalizacja pliku na repozytorium\n" \
            "-- ./client.py rm  <lokalizacja pliku na repozytorium\n" \
            "-- ./client.py mv <lokalizacja bazowa> <lokalizacja docelowa>\n"\
            "-- ./client.py ls <lokalizacja pliku>"
        else: 
            print "Brak takiej operacji" 
        

    def addFile(self,selection):
        if len(selection) == 2:
            try:
                f = open(selection[1], 'rb')
                data = f.read()
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                print "Sprobuj jeszcze raz"
                return 
            #TODO: regex sama nazwa
            request = AddFileRequest(selection[0], selection[1], data)
            try:
                helloclient, fileclient = self.clientconn.start()
                try:
                    response = fileclient.addFile(request)
                    print "Dodawanie: " + selection[0] + "/" + selection[1] +" Status: "+ ResponseStatus._VALUES_TO_NAMES[response.status]
                except TTransport.TTransportException as e:
                     print "Dodawanie: Brak odpowiedzi: %s" % (e.message)
                except Thrift.TApplicationException as e:
                     print "Dodawanie: Problem przetwarzania pliku na serwerze: %s" % (e.message)                    
            except TypeError as e:
                print "%s" % (e.message)
            f.close()
       

    def getFile(self,selection):
        request = GetFileRequest(selection[0])
        try:
            helloclient, fileclient = self.clientconn.start()
            response = fileclient.getFile(request)
            print "Pobranie: " + selection[0] + " Status: "+ ResponseStatus._VALUES_TO_NAMES[response.status]
    #!! plik bedzie nadpisywany!
            if ResponseStatus._VALUES_TO_NAMES[response.status] == 'OK':
                try:
                    f = open(response.fileName, 'w')
                    f.write(response.fileData)
                    f.close()
                except IOError as e:
                    print "Pobranie: I/O error({0}): {1}".format(e.errno, e.strerror)
            self.clientconn.stop()
        except TypeError as e:
            print "Pobranie: Brak polaczenia"
            print "%s" % (e.message)
        
    def rmFile(self,selection):
        request = RemoveFileRequest(selection[0])
        try:
            helloclient, fileclient = self.clientconn.start()
            response = fileclient.removeFile(request)
            print "Usuwanie: " + selection[0] +" Status: "+ ResponseStatus._VALUES_TO_NAMES[response.status]
            self.clientconn.stop()
        except TypeError as e:
            print "Usuwanie: Brak polaczenia"
            print "%s" % (e.message)
        
    def mvFile(self,selection):
        request = MoveFileRequest(selection[0], selection[1])
        try:
            helloclient, fileclient = self.clientconn.start()
            response = fileclient.moveFile(request)
            print "Status: "+ ResponseStatus._VALUES_TO_NAMES[response.status]
            self.clientconn.stop()
        except TypeError as e:
            print "Brak polaczenia"
            print "%s" % (e.message)     
        
    def lsDir(self,selection):
        request = ListDirRequest(selection[0])
        try:
            helloclient, fileclient = self.clientconn.start()
            response = fileclient.listDir(request)

            print "LS: Status: "+ ResponseStatus._VALUES_TO_NAMES[response.status]
            print "\nLista:"
            if not response.result:
                print "<lista jest pusta>"
            else:
                for item in response.result:
                    print item
            self.clientconn.stop()
        except TypeError as e:
            print "LS: Brak polaczenia"
        

menu = Menu()
menu.choice()
