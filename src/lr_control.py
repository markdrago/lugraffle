#Licensed under the MIT license
#Copyright (c) 2008 Mark Drago <markdrago@gmail.com>

import logging

class LRControl:
    singleton = None
    
    @classmethod
    def get_control(cls):
        if cls.singleton is None:
            cls.singleton = LRControl()
        return cls.singleton

    def __init__(self):
        self.logger = logging.getLogger('LR.LRControl')
        self.listeners = []

    def register(self, obj):
        self.listeners.append(obj)

    def initiate_drawing(self):
        self.dispatch('initiate_drawing_cb')

    def dispatch(self, methodname, params=None):
        for obj in self.listeners:
            method = getattr(obj, methodname, None)
            if callable(method):
                if params is not None:
                    method(**params)
                else:
                    method()
