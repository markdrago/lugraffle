#Licensed under the MIT license
#Copyright (c) 2008 Mark Drago <markdrago@gmail.com>

import logging
import random
import sha

# 2^32 - 1 (max 32 bit integer)
RANDMAX = 4294967295

class LRDrawing:
    def __init__(self):
        self.randomint = random.randint(0, RANDMAX)
        sha1 = sha.new("%d" % self.randomint)
        self.hash = sha1.hexdigest()
    
    def get_random_int(self):
        return self.randomint

    def get_hash(self):
        return self.hash
