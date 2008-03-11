#!/usr/bin/env python
#Licensed under the MIT license
#Copyright (c) 2008 Mark Drago <markdrago@gmail.com>

import logging, sys, readline, shlex
import dbus

class LRTerm():
    def __init__(self):
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
	self.cmds = {"ls" : [ [0, 1], self.ls,
		      "[<item>] list all items or entries for an item"],
		     "touch" : [ [1], self.touch,
		      "[item/entry] add entry to item"],
		     "mkdir" : [ [1], self.mkdir, "[item] add item"],
		     "help" : [ [0], self.help, "show this help output"],
		     "exit" : [ [0], self.exit, "exit"],
		     "q" : [ [0], self.exit, "exit"]}

    def main(self):
	while 1:
	    (cmd, args) = self.get_command()
	    self.cmds[cmd][1](args)

    def exit(self, args):
	exit(0)

    def ls(self, args):
	if args is None:
	    self.print_items()
	elif args[0] == '*':
	    self.print_items_and_entries()
	else:
	    self.print_entries_for_item(args[0])

    def touch(self, args):
	parts = args[0].split('/')
	if len(parts) != 2:
	    return
	self.add_entry(parts[0], parts[1])

    def mkdir(self, args):
	self.add_item(args[0])

    def help(self, args):
	print "Commands:"
	for cmd in self.cmds.keys():
	    print "%s\t-- %s" % (cmd, self.cmds[cmd][2])

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

    def get_command(self):
	#get a legal command
	cmd = ""
	while cmd not in self.cmds.keys():
	    line = raw_input("lr> ")
	    pieces = shlex.split(line)
	    if len(pieces) > 0:
		cmd = pieces[0]

	#make sure we have a legal # of arguments for this command
	if (len(pieces) - 1) in self.cmds[cmd][0]:
	    if len(pieces) > 1:
		args = pieces[1:]
	    else:
		args = None
	else:
	    return self.get_command()

	return (cmd, args)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
			format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
			datefmt='%H:%M:%S',
			stream=sys.stderr)

    lrterm = LRTerm()
    lrterm.main()
