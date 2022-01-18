from matplotlib import pyplot as plt
import numpy as np

class Visualizer:
    def __init__(self, model):
        self._model = model
        self._nodes = self._model.getNodes()
        self._elements = self._model.getElements()
        self._meshNodes = self._model.getMeshNodes()
        self._meshElements = self._model.getMeshElements()

        self.scale = 50

    def drawModel(self, show=True):
        for ID, element in self._elements.items():
            coordinates = np.vstack([node.getPosition() for node in element.getNodes()])
            plt.plot(coordinates[:,0], coordinates[:,1], '-k', marker='o')
        if show:
            plt.show()


    def drawDisplacement(self, drawUndeformated=True):
        for ID, element in self._meshElements.items():
            displacement = np.vstack([node.getDisplacement() for node in element.getNodes()])
            coordinates = np.vstack([node.getPosition() for node in element.getNodes()])
            positionX = coordinates[:, 0] + displacement[:, 0] * self.scale
            positionY = coordinates[:, 1] + displacement[:, 1] * self.scale

            plt.plot(positionX, positionY, '-y')

        if drawUndeformated:
            self.drawModel(False)
        plt.show()

