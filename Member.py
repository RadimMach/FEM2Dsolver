import numpy as np


class Member:

    def __init__(self, ID, nodes, section, hinges=[False, False]):
        self.ID = ID
        self._section = section
        self.nodes = nodes
        self.hinges = hinges

    def getLength(self):
        return np.linalg.norm([x.getPosition() - y.getPosition() for x, y in zip(self.nodes, self.nodes[1:])])

    def computeLocalStiffnessMatrix(self):
        E = self._section.getEModulus()
        A = self._section.getArea()
        I = self._section.getInertiaMoment()
        L = self.getLength()

        Kfixfix = np.array([
            [E * A / L, 0, 0,                                   - E * A / L, 0, 0],
            [0, 12 * E * I / L ** 3, 6 * E * I / L ** 2,        0, - 12 * E * I / L ** 3, 6 * E * I / L ** 2],
            [0, 6 * E * I / L ** 2, 4 * E * I / L,              0, - 6 * E * I / L ** 2, 2 * E * I / L],
            [-E * A / L, 0, 0,                                  E * A / L, 0, 0],
            [0, - 12 * E * I / L ** 3, - 6 * E * I / L ** 2,    0, 12 * E * I / L ** 3, - 6 * E * I / L ** 2],
            [0, 6 * E * I / L ** 2, 2 * E * I / L,              0, - 6 * E * I / L ** 2, 4 * E * I / L]])

        Kpinfix = np.array([
            [E * A / L, 0, 0,               - E * A / L, 0, 0],
            [0, 3 * E * I / L ** 3, 0,      0, - 3 * E * I / L ** 3, 3 * E * I / L ** 2],
            [0, 0, 0,                       0, 0, 0],
            [-E * A / L, 0, 0,              E * A / L, 0, 0],
            [0, - 3 * E * I / L ** 3, 0,    0, 3 * E * I / L ** 3, - 3 * E * I / L ** 2],
            [0, 3 * E * I / L ** 2, 0,      0, - 3 * E * I / L ** 2, 3 * E * I / L]])

        Kfixpin = np.array([
            [E * A / L, 0, 0,                               - E * A / L, 0, 0],
            [0, 3 * E * I / L ** 3, 3 * E * I / L ** 2,     0, - 3 * E * I / L ** 3, 0],
            [0, 3 * E * I / L ** 2, 3 * E * I / L,          0, - 3 * E * I / L ** 2, 0],
            [-E * A / L, 0, 0,                              E * A / L, 0, 0],
            [0, - 3 * E * I / L ** 3, -3 * E * I / L ** 2,  0, 3 * E * I / L ** 3, 0],
            [0, 0, 0,                                       0, 0, 0]])

        Kpinpin = np.array([
            [E * A / L, 0, 0,   - E * A / L, 0, 0],
            [0, 0, 0,           0, 0, 0],
            [0, 0, 0,           0, 0, 0],
            [-E * A / L, 0, 0,  E * A / L, 0, 0],
            [0, 0, 0,           0, 0, 0],
            [0, 0, 0,           0, 0, 0]])

        if all(self.hinges):
            return Kpinpin
        elif not any(self.hinges):
            return Kfixfix
        elif self.hinges[0]:
            return Kpinfix
        elif self.hinges[1]:
            return Kfixpin


    def _getTransformationMatrix(self):
        c, s = np.subtract(self.nodes[1].getPosition(), self.nodes[0].getPosition()) / self.getLength()

        t = np.array([[c, s, 0, 0, 0, 0],
                      [-s, c, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0],
                      [0, 0, 0, c, s, 0],
                      [0, 0, 0, -s, c, 0],
                      [0, 0, 0, 0, 0, 1]])
        return t

    def getStiffnessMatrix(self):
        t = self._getTransformationMatrix()
        return t.T @ self.computeLocalStiffnessMatrix() @ t

    def getNodesId(self):
        return [node._ID for node in self.nodes]

    def getID(self):
        return self.ID

    def getNodes(self):
        return self.nodes

    def getSection(self):
        return self._section

    def setHinges(self, hinges):
        self.hinges = hinges

    def getHinges(self):
        return self.hinges
