import sys, os
sys.path.append('./gen-py')
 
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from services import HelloFriend
from services import FileResourceService

from server import Server

SERVICE_TIMEOUT_IN_mS = 300

# Ustanaiwanie polaczenia z serwerem

class ClientConnection:
    transport = ''
    server = ''
    def __init__(self):
        self.log = {}
        self.server = Server()
    
    def start(self):
        retry = False
        socket = self.server.getServer()
        while socket != 0:
            if retry == True:
                socket = self.server.nextServer()
                if socket == 0:
                    print "Usluga niedostepna"
                    break
            
            host = socket['ip']
            port = socket['client_service_port']
            try:
              # Make socket
                self.transport = TSocket.TSocket(host, port)
            
                #self.transport.setTimeout(SERVICE_TIMEOUT_IN_mS)
              # Buffering is critical. Raw sockets are very slow
                self.transport = TTransport.TBufferedTransport(self.transport)
             
              # Wrap in a protocol
                protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
             
              # Create a client to use the protocol encoder
                client = HelloFriend.Client(protocol)
                client2 = FileResourceService.Client(protocol)
              # Connect!
                k = self.transport.open()
                print "Rozmawialem z: " +  socket['ip'] + ':' + str(socket['client_service_port'])
                #client.ping()
                #print "ping()"
                #msg = client.sayHello()
                #print msg
                
                return client, client2
            except Thrift.TException, tx:
                retry = True
                print "%s" % (tx.message)

    def stop(self):
        try:
            self.transport.close()
        except Thrift.TException, tx:
            print "%s" % (tx.message)