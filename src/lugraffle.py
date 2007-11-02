from twisted.internet.protocol import DatagramProtocol
from socket import *

#import reactor stuff, tell it to use the glib2 main loop for dbus support
from twisted.internet import glib2reactor
glib2reactor.install()
from twisted.internet import reactor

#define what we should do when we receive a packet
class LRServer(DatagramProtocol):
    sendport = 1234
    sendhost = "<broadcast>"

    def startProtocol(self):
        self.sendsocket = socket(AF_INET, SOCK_DGRAM)
        self.sendsocket.bind(('', 0))
        self.sendsocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)

        #we should not respond to packets that we sent ourselves
        #if (host == ################):
        #    print "not replying to packet from self"
        #    return
        
        self.sendsocket.sendto(data, (self.sendhost, self.sendport))

#start listening for connections on our udp port
if __name__ == '__main__':
    reactor.listenUDP(1234, LRServer())
    reactor.run()
