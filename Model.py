from Node import Node
from Member import Member
from Section import Section

from NodalSupport import NodalSupport
from NodalForce import NodalForce
import numpy as np

class Model:
    def __init__(self):
        self.nodes = {}
        self.elements = {}
        self.meshNodes = {}
        self.meshElements = {}

    def createNode(self, ID, coordinates):
        node = Node(ID, coordinates)
        self.addNode(node)

    def addNode(self, node):
        self.nodes[node.getID()] = node

    def addElement(self, element):
        self.elements[element.getID()] = element

    def addNodes(self, nodes):
        for node in nodes:
            self.addNode(node)

    def createElement(self, ID, nodes, section, hinges):
        section = Section()
        hinges = [False, False]
        member = Member(ID, nodes, section, hinges)
        self.addElement(member)

    def addElements(self, elements):
        for element in elements:
            self.addElement(element)

    def getElements(self):
        return self.elements

    def getNodes(self):
        return self.nodes

    def getMeshElements(self):
        return self.meshElements

    def getMeshNodes(self):
        return self.meshNodes

    def assembleLoadVector(self):
        fGlobal = []
        for ID, node in self.meshNodes.items():
            if node._nodalForces:
                fGlobal.extend(node.getNodalForce())
            else:
                for _ in range(node.getDOFNumber()): #DOF
                    fGlobal.append(0)

        return np.array(fGlobal)

    def assembleStiffnessMatrix(self):
        nDOF = self.nodes[0].getDOFNumber()
        taskSize = len(self.meshNodes) * nDOF
        kGlobal = np.zeros([taskSize, taskSize])

        for ID, element in self.meshElements.items():
            k = element.getStiffnessMatrix()
            for countRow, row in enumerate(element.getNodesId()):
                for countColumn, column in enumerate(element.getNodesId()):
                    rowGlobal = slice(row * nDOF, row * nDOF + nDOF)
                    columnGlobal = slice(column * nDOF, column * nDOF + nDOF)
                    rowLocal = slice(nDOF * countRow, nDOF * countRow + nDOF)
                    columnLocal = slice(nDOF * countColumn, nDOF * countColumn + nDOF)

                    kGlobal[rowGlobal, columnGlobal] += k[rowLocal, columnLocal]

        for ID, node in self.meshNodes.items():
            supports = node.getNodalSupport()
            for degree in range(node.getDOFNumber()):
                if supports and supports.getConstrains()[degree]:
                    position = ID * node.getDOFNumber() + degree
                    kGlobal[:, position] = 0
                    kGlobal[position, :] = 0
                    kGlobal[position, position] = 1

        return kGlobal

    def solve(self):
        K = self.assembleStiffnessMatrix()
        F = self.assembleLoadVector()
        self.u = np.linalg.inv(K) @ F
        self.assignDisplacement()

        return self.u

    def assignDisplacement(self):
        nodeStart = 0
        for ID, node in self.meshNodes.items():
            node.setDisplacement([self.u[nodeStart + degree] for degree in range(node.getDOFNumber())])
            nodeStart += node.getDOFNumber()

    def generateMesh(self, numberOfDivisions = 1):
        self.meshNodes = self.nodes.copy()
        meshNodeCount = len(self.meshNodes)
        meshElementCount = 1

        if numberOfDivisions == 1:
            self.meshElements = self.elements.copy()
        else:
            for _, element in self.elements.items():
                nodes = element.getNodes()
                increment = (nodes[1].getPosition() - nodes[0].getPosition()) / numberOfDivisions
                lastMeshNode = nodes[0]
                section = element.getSection()
                elementHinges = element.getHinges()

                for node in range(numberOfDivisions - 1):
                    # New mesh node
                    nextMeshNode = Node(meshNodeCount, lastMeshNode.getPosition() + increment)
                    self.meshNodes[meshNodeCount] = nextMeshNode

                    # New mesh element
                    meshElement = Member(meshElementCount, [lastMeshNode, nextMeshNode], section)
                    self.meshElements[meshElementCount] = meshElement

                    # Handle member hinge at start node
                    if node == 0:
                        meshElement.setHinges([elementHinges[0], False])

                    # Increase for next loop
                    lastMeshNode = nextMeshNode
                    meshNodeCount += 1
                    meshElementCount += 1

                # Create element to connect with end node
                meshElement = Member(meshElementCount , [lastMeshNode, nodes[1]], section)
                meshElement.setHinges([False, elementHinges[1]])
                self.meshElements[meshElementCount] = meshElement
                meshElementCount += 1
