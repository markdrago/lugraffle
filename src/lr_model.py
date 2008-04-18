#!/usr/bin/env python
#Licensed under the MIT license
#Copyright (c) 2007, 2008 Mark Drago <markdrago@gmail.com>

import logging

class LRModel:
    singleton = None
    
    def get_model(cls):
        if cls.singleton is None:
            cls.singleton = LRModel()
        return cls.singleton
    get_model = classmethod(get_model)

    def __init__(self):
        self.logger = logging.getLogger('LR.LRModel')
        self.items = {}
        self.listeners = {}

    #The model will optionally tell listeners about actions
    #that they were responsible for adding.  This is done by giving
    #each listener a name and requiring that a name be passed to the
    #model when items or entries are added.  The send_self_changes
    #parameter allows some listeners to override the protection.
    def register_listener(self, name, func, send_self_changes = False):
        self.listeners[name] = (func, send_self_changes)

    def add_item(self, src, item_name):
        #add item
        if item_name not in self.items:
            self.items[item_name] = []
            self.notify_listeners(src, item_name, None)

    def add_entry(self, src, item_name, entry_name):
        #add entry
        if item_name in self.items:
            if entry_name not in self.items[item_name]:
                self.items[item_name].append(entry_name)
                self.notify_listeners(src, item_name, entry_name)

    def get_items(self):
        return self.items.keys()

    def get_entries_for_item(self, item_name):
        return self.items.get(item_name)

    def get_items_and_entries(self):
        return self.items

    def notify_listeners(self, src, item, entry):
        for listener in self.listeners.keys():
            if listener == src and not self.listeners[listener][1]:
                continue
            self.listeners[listener][0](item, entry)

    def dump_model_state(self):
        self.logger.info("Model:")
        for item in self.get_items():
            self.logger.info("%s" % item)
            for entry in self.get_entries_for_item(item):
                self.logger.info("    %s" % entry)
