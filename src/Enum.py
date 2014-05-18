class Enum(object):
    """docstring for Enum"""
    def __init__(self):
        super(Enum, self).__init__()
        self.lastId = 0
    def addId(self):
        self.lastId +=1
        return self.lastId

Enum = Enum()
