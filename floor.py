class Floor(object):
    _is_solid = False

    def __init__(self):
        super(Floor, self).__init__()

    def is_solid(self):
        return _is_solid

