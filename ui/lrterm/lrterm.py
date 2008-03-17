#!/usr/bin/env python
#Licensed under the MIT license
#Copyright (c) 2008 Mark Drago <markdrago@gmail.com>

import logging, sys
import dbus
from cmd import Cmd

class LRTerm(Cmd):
    prompt = 'lr> '
    def __init__(self):
	Cmd.__init__(self)
	self.logger = logging.getLogger('LRTerm')
	self.dbus_bus = dbus.SessionBus()
	try:
	    self.dbus_obj = self.dbus_bus.get_object('org.lilug.lugraffle', '/')
	except dbus.exceptions.DBusException:
	    print "Unable to connect to the org.lilug.lugraffle DBus service."
	    print "Are you sure that lugraffled is running?"
	    exit(1)
	self.dbus_iface = dbus.Interface(self.dbus_obj,
					 dbus_interface='org.lilug.lugraffle')

    def exit(self, args=None):
	exit(0)

    def do_EOF(self, x):
	"""Exit"""
	print
	print "Goodbye!"
	self.exit()

    def do_ls(self, item):
	"""ls [<item>]
	list all items or entries for an item"""
	if not item:
	    self.print_items()
	elif item == '*':
	    self.print_items_and_entries()
	else:
	    self.print_entries_for_item(item)
 
    def complete_ls(self, text, line, begidx, endidx):
	return [i for i in self.dbus_iface.get_items() if i.startswith(text)]

    complete_touch = complete_ls
  
    def do_touch(self, arg):
	"""touch [item/entry]
	add entry to item"""
	parts = arg.split('/')
	if len(parts) != 2:
	    return
	self.add_entry(parts[0], parts[1])
  
    def do_mkdir(self, item):
	"""mkdir item
	add item"""
	self.add_item(item)

    def add_item(self, item):
	self.dbus_iface.add_item(item)

    def add_entry(self, item, entry):
	self.dbus_iface.add_entry(item, entry)

    def print_entries_for_item(self, item):
	for entry in self.dbus_iface.get_entries_for_item(item):
	    print "%s" % entry

    def print_items(self):
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
			format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
			datefmt='%H:%M:%S',
			stream=sys.stderr)

    lrterm = LRTerm()
    lrterm.cmdloop()
