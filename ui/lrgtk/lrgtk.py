#!/usr/bin/env python

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
	gladefile = 'lrgtk.glade'
	windowname = 'main_window'
	self.gladedoc = gtk.glade.XML(gladefile, windowname)
	self.gladedoc.signal_autoconnect(self)
	self.main_window = self.gladedoc.get_widget('main_window')
	self.main_window.connect("delete_event", self.exit)

    def main(self):
	self.main_window.show()
	gtk.main()

    def exit(self, widget, event):
	gtk.main_quit()
	exit(0)

if __name__ == '__main__':
    lrgtk = LRGtk()
    lrgtk.main()
