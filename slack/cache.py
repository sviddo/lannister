import copy

class Cache:
    data = {}

    def add(self, data_name, data):
        self.data[data_name] = data

    def update(self, data_name, data):
            self.data[data_name] = data

    def get(self, data_name):
        return copy.deepcopy(self.data[data_name])

    def get_mutable(self, data_name):
        return self.data[data_name]

    def delte(self, data_name):
        del(self.data[data_name])
    
    def pop(self, data_name):
        return self.data.pop(data_name)