import logging, sys, readline
import dbus

class LRTerm():
    def __init__(self):
	self.logger = logging.getLogger('LRTerm')
	self.dbus_bus = dbus.SessionBus()
	self.dbus_obj = self.dbus_bus.get_object('org.lilug.lugraffle', '/')
	self.dbus_iface = dbus.Interface(self.dbus_obj,
					 dbus_interface='org.lilug.lugraffle')
	self.cmds = [["ls", [0, 1], self.ls,
		      "[<item>] list all items or entries for an item"],
#		     ["touch", [1], self.touch,
#		      "[item/entry] add entry to item"],
#		     ["mkdir", [1], self.mkdir,
#		      "[item] add item"],
		     ["help", [0], self.help, "show this help output"],
		     ["exit", [0], self.exit, "exit"],
		     ["q", [0], self.exit, "exit"]]

    def main(self):
	while 1:
	    (cmd, args) = self.get_command()
	    if cmd == "ls":
		self.print_items(None)
	    elif cmd == "help":
		self.help()
	    elif cmd == "exit" or cmd == "q":
		self.exit()
#	    elif cmd == "ls items":
#		self.print_items()


    def exit(self):
	exit(0)

    def ls(self, item):
	if item is None:
	    self.print_items_and_entries()
	else:
	    self.print_items()

    def help(self):
	print "Commands:"
	for tpl in self.cmds:
	    print "%s\t-- %s" % (tpl[0], tpl[3])

    def print_items():
	for item in self.dbus_iface.get_items():
	    print "%s" % item

    def print_items_and_entries(self):
	model = self.dbus_iface.get_items_and_entries()
	for item in model.keys():
	    print "%s:" % item,
	    sep = ""
	    for entry in model[item]:
		print "%s%s" % (sep, entry),
		sep = ", "
	    print ""

    def get_command(self):
	#get list of all legal commands
	allowed_cmds = []
	for tpl in self.cmds:
	    allowed_cmds.append(tpl[0])

	#get a legal command
	cmd = ""
	while cmd not in allowed_cmds:
	    cmd = raw_input("lr> ")

	return (cmd, None)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
			format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
			datefmt='%H:%M:%S',
			stream=sys.stderr)

    lrterm = LRTerm()
    lrterm.main()
