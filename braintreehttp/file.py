class File(object):

    @classmethod
    def fromhandle(cls, handle):
        return File(handle.name, handle.mode)

    def __init__(self, name, mode='rb'):
        self._handle = None

        self.mode = mode
        self.closed = False
        self.name = name

    def read(self):
        self.open()

        return self._handle.read()

    def close(self):
        if self._handle:
            self._handle.close()
            self._handle = None
            self.closed = True

    def open(self):
        if not self._handle:
            if not self.closed:
                self._handle = open(self.name, self.mode)
            else:
                raise IOError('Open of closed file')
