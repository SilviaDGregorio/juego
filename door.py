class Door(object):
    _is_solid = True

    def __init__(self):
        super(Door, self).__init__()
        
    def is_solid(self):
        return _is_solid

