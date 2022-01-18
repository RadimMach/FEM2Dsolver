class Section:
    def __init__(self):
        # For now default values
        self.E = 210e9
        self.bx = 0.001
        self.hx = 0.2
        self.A = self.bx * self.hx
        self.I = (1 / 12) * self.bx * (self.hx ** 3)

    def getArea(self):
        return self.A

    def getEModulus(self):
        return self.E

    def getInertiaMoment(self):
        return self.I