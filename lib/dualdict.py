class ReverseDictionary(object):
    def __init__(self):
        self.forwards = dict()
        self.reverse = dict()
    def __setitem__(self, key, value):
        self.forwards[key] = value
        self.reverse[value] = key
    def __getitem__(self, key):
        return self.forwards[key]
    def get(self, key):
        return self.forwards[key]
    def rget(self, val):
        return self.reverse[val]
    def __contains__(self, key):
        return key in self.forwards
    def __iter__(self):
        return self.forwards.items()
    
