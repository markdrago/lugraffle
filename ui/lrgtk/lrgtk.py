#!/usr/bin/env python

import logging, sys
import dbus
import dbus.glib

#import pygtk
try:
    import pygtk
    pygtk.require("2.0")
    import gtk
    import gtk.glade
except:
    print "Unable to load pygtk."
    print "You should install pygtk >= 2.0 and try again."
    exit(1)

class LRGtk:
    def __init__(self):
        self.logger = logging.getLogger('LRGtk')
        self.init_gtk()
        self.init_dbus()

    def init_gtk(self):
        #load glade file
        gladefile = 'lrgtk.glade'
        self.gladedoc = gtk.glade.XML(gladefile, 'main_window')
        self.gladedoc.signal_autoconnect(self)

        #add event to close window
        self.main_window = self.gladedoc.get_widget('main_window')
        self.main_window.connect("delete_event", self.exit)

        #create treestore
        self.tree_store = gtk.TreeStore(str)
        tree_view = self.gladedoc.get_widget('model_tree_view')
        tree_view.set_model(self.tree_store)
        tree_view.set_headers_visible(True)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Name", renderer, text=0)
        tree_view.append_column(column)

    def init_dbus(self):
        self.dbus_bus = dbus.SessionBus()
        try:
            self.dbus_obj = self.dbus_bus.get_object('org.lilug.lugraffle','/')
        except dbus.exceptions.DBusException:
            print "Unable to connect to the org.lilug.lugraffle DBus service."
            print "Are you sure that lugraffled is running?"
            exit(1)
        self.dbus_iface = dbus.Interface(self.dbus_obj,
                                         dbus_interface='org.lilug.lugraffle')
        self.dbus_iface.connect_to_signal('item_added', self.item_added)

    def main(self):
        self.main_window.show()
        gtk.main()

    def item_added(self, item):
        self.tree_store.append(None, (item,))
        
    def exit(self, widget, event):
        gtk.main_quit()
        exit(0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%H:%M:%S',
                        stream=sys.stderr)
    lrgtk = LRGtk()
    lrgtk.main()
