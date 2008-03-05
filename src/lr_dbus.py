#Licensed under the MIT license
#Copyright (c) 2008 Mark Drago <markdrago@gmail.com>

import dbus
import dbus.service
import dbus.glib
import utils
import logging
from lr_model import *

#network interface for lug raffle
class LRDBus(dbus.service.Object):
    def __init__(self, reactor):
	self.model = LRModel.get_model()
	self.logger = logging.getLogger('LR.LRDBus')
	self.bus = dbus.SessionBus()
	self.name = dbus.service.BusName('org.lilug.lugraffle')
	dbus.service.Object.__init__(self, self.bus, '/org/lilug/lugraffle')

    @dbus.service.method('org.lilug.lugraffle')
    def ping(self):
	return "pong"
