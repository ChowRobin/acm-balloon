class person:
    def __init__(self, name, xh):
        self._name = name
        self._xh = xh
        self._position = None
        self.acObj = {}
        self.Balloon = {}
        self.initStatus()

    def initStatus(self):
        for i in range(1, 9):
            self.acObj[i] = False
            self.Balloon[i] = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def xh(self):
        return self._xh

    @xh.setter
    def xh(self, xh):
        self._xh = xh
    
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        if isinstance(position, str):
            self._position = position

    def acStatus(self, id):
        return self.acObj[id]

    def ac(self, id):
        self.acObj[id] = True

    def balloonStatus(self, id):
        return self.Balloon[id]

    def getBalloon(self, id):
        self.Balloon[id] = True