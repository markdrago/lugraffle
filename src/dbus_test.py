import logging, sys
import dbus, dbus.service, dbus.glib, gobject
from dbus.mainloop.glib import DBusGMainLoop

class DBusTest():
    def __init__(self):
	self.logger = logging.getLogger('LR.DBusTest')
	DBusGMainLoop(set_as_default = True)
	self.loop = gobject.MainLoop()
	self.bus = dbus.SessionBus()
	self.bus.add_signal_receiver(self.got_item, "item_added",
				     "org.lilug.lugraffle",
				     "org.lilug.lugraffle", "/")
	self.bus.add_signal_receiver(self.got_entry, "entry_added",
				     "org.lilug.lugraffle",
				     "org.lilug.lugraffle", "/")

    def run_test(self):
	self.loop.run()

    def got_item(self, item):
	self.logger.info("Received Item: %s" % item)

    def got_entry(self, item, entry):
	self.logger.info("Received Entry: %s, %s" % (item, entry))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
			format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
			datefmt='%H:%M:%S',
			stream=sys.stderr)

    tester = DBusTest()
    tester.run_test()
