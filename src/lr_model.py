
class LRModel():

    def __init__(self):
	self.items = {}

    def add_item(self, item_name):
	if item_name not in self.items:
	    self.items[item_name] = []

    def add_entry(self, item_name, entry_name):
	if item_name in self.items:
	    if entry_name not in self.items[item_name]:
		self.items[item_name].append(entry_name)

    def get_items(self):
	return self.items.keys()

    def get_entries_for_item(self, item_name):
	if item_name in self.items:
	    return self.items[item_name]
