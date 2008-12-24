#!/usr/bin/env python
#Licensed under the MIT license
#Copyright (c) 2008 Mark Drago <markdrago@gmail.com>

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
        self.list = LRGtk_List(self.tree_view)
        self.init_dbus()
        self.init_tree()
        self.main_window.show()

    def init_gtk(self):
        gladefile = 'lrgtk.glade'
        self.main_win = gtk.glade.XML(gladefile, 'main_window')
        self.main_win.signal_autoconnect(self)
        self.main_window = self.main_win.get_widget('main_window')
        self.tree_view = self.main_win.get_widget('model_tree_view')

        self.add_item_win = gtk.glade.XML(gladefile, 'add_item_dialog')
        self.add_item_win.signal_autoconnect(self)
        self.add_item_dialog = self.add_item_win.get_widget('add_item_dialog')
        self.add_item_entry = self.add_item_win.get_widget('add_item_name_entry')

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
        self.dbus_iface.connect_to_signal('item_added', self.list.add_item)
        self.dbus_iface.connect_to_signal('entry_added', self.list.add_entry)

    def show_add_item_dialog(self, event):
        self.add_item_dialog.show()

    def hide_add_item_dialog(self, widget, event=None):
        self.add_item_dialog.hide()
        return True

    def add_item(self, widget):
        item = self.add_item_entry.get_text()
        if item != None and item != "":
            self.dbus_iface.add_item(item)

    def init_tree(self):
        model = self.dbus_iface.get_items_and_entries()
        for item in model.keys():
            self.list.add_item(item)
            for entry in model[item]:
                self.list.add_entry(item, entry)

    def exit(self, widget, event):
        gtk.main_quit()
        exit(0)

class LRGtk_List:
    def __init__(self, tree_view):
        self.logger = logging.getLogger('LRGtk_List')
        #create treestore
        self.tree_view = tree_view
        self.tree_store = gtk.TreeStore(str)
        self.tree_view.set_model(self.tree_store)
        self.tree_view.set_headers_visible(False)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Name", renderer, text=0)
        self.tree_view.append_column(column)

    def add_item(self, item):
        item_iter = self.find_item(item)
        if item_iter is not None:
            self.logger.debug("Item already exists: %s" % item)
            return
        self.tree_store.append(None, (item,))

    def add_entry(self, item, entry):
        item_iter = self.find_item(item)
        if item_iter is None:
            self.logger.debug("No item found with name: %s" % item)
            return
        entry_iter = self.find_entry(item_iter, entry)
        if entry_iter is not None:
            self.logger.debug("Item already has entry: (%s, %s)" % (item, entry))
            return
        self.tree_store.append(item_iter, (entry,))

    def find_entry(self, item_iter, entry):
        entry_iter = self.tree_store.iter_children(item_iter)
        while entry_iter is not None:
            if self.tree_store.get_value(entry_iter, 0) == entry:
                return entry_iter
            entry_iter = self.tree_store.iter_next(entry_iter)
        return None

    def find_item(self, item):
        tree_iter = None
        while True:
            #get the first or the next item
            if tree_iter is None:
                tree_iter = self.tree_store.get_iter_root()
            else:
                tree_iter = self.tree_store.iter_next(tree_iter)

            #if we get to the end of the list
            if tree_iter is None:
                break

            #if we found what we were looking for
            if item == self.tree_store.get_value(tree_iter, 0):
                return tree_iter
        return None

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%H:%M:%S',
                        stream=sys.stderr)
    lrgtk = LRGtk()
    gtk.main()
