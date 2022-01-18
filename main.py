from Node import *
from Member import Member
from Section import Section
from Model import Model
from Visualizer import Visualizer

# Nodes
nodesCoordinates = [[0, 0],
                    [0, 1],
                    [0, 2],
                    [0, 3],
                    [1, 3],
                    [2, 3],
                    [3, 3],
                    [4, 3],
                    [5, 3],
                    [5, 2],
                    [5, 1],
                    [5, 0]]

nodes = [Node(ID, inputs) for ID, inputs in enumerate(nodesCoordinates)]

# Members
memberInput = [[0, 1],
               [1, 2],
               [2, 3],
               [3, 4],
               [4, 5],
               [5, 6],
               [6, 7],
               [7, 8],
               [8, 9],
               [9, 10],
               [10, 11]]

section = Section() # Section
members = [Member(ID, [nodes[element[0]], nodes[element[1]]], section) for ID, element in enumerate(memberInput)]
members[9].hinges = [True, False] # Hinges

# Nodal supports
nodalSupport = {0:  [True, True, True],
                11: [True, True, True]}

[nodes[key].setNodalSupport(items) for key, items in nodalSupport.items()]

# Nodal forces
nodalForce = {1: [500, 0, 0],
              2: [500, 0, 0],
              3: [0, -500, 0],
              4: [0, -1000, 0],
              5: [0, -2000, 0],
              7: [0, -1000, 0],
              8: [0, -500, 0]}

[nodes[key].setNodalForce(items) for key, items in nodalForce.items()]

# Create model
model = Model()
model.addNodes(nodes)
model.addElements(members)

# Generate mesh and calculate
model.generateMesh(2)
model.solve()

# Show results
visualizer = Visualizer(model)
visualizer.drawDisplacement()


