import dbus
import dbus.service
import dbus.glib
import utils
import logging

#network interface for lug raffle
class LRDBus(dbus.service.Object):
    def __init__(self, model, reactor):
	self.model = model
	self.logger = logging.getLogger('LR.LRServer')
	self.bus = dbus.SessionBus()
	self.name = dbus.service.BusName('org.lilug.lugraffle')
	dbus.service.Object.__init__(self, self.bus, '/org/lilug/lugraffle')

    @dbus.service.method('org.lilug.lugraffle')
    def ping(self):
	return "pong"
