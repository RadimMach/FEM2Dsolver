import numpy as np
from NodalForce import *
from NodalSupport import *

class Node:
    def __init__(self, ID, position):
        self.position = position
        self._ID = ID
        self._nodalForces = None
        self._nodalSupport = None
        self._displacement = None

    def getPosition(self):
        return np.array(self.position)

    def setNodalForce(self, forces):
        self._nodalForces = NodalForce(forces)

    def getNodalForce(self):
        return self._nodalForces.getForces()

    def setNodalSupport(self, supports):
        self._nodalSupport = NodalSupport(supports)

    def getNodalSupport(self):
        return self._nodalSupport

    def setDisplacement(self, displacement):
        self._displacement = displacement

    def getDisplacement(self):
        return self._displacement

    def getDOFNumber(self):
        #right now only for 2D
        return 3

    def getID(self):
        return self._ID




