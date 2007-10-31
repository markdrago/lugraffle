from twisted.internet.protocol import DatagramProtocol

#import reactor stuff, tell it to use the glib2 main loop for dbus support
from twisted.internet import glib2reactor
glib2reactor.install()
from twisted.internet import reactor

#define what we should do when we receive a packet
class LRServer(DatagramProtocol):
    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        self.transport.write(data, (host, port))

#start listening for connections on our udp port
if __name__ == '__main__':
    reactor.listenUDP(1234, LRServer())
    reactor.run()
