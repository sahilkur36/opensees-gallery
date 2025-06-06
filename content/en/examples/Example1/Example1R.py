# OpenSees -- Open System for Earthquake Engineering Simulation
# Pacific Earthquake Engineering Research Center
# http://opensees.berkeley.edu/
#
# Basic Truss Example 1.1
# -----------------------
#  2d 3 Element Elastic Truss
#  Single Nodal Load, Static Analysis
#
# Written: Andreas Schellenberg (andreas.schellenberg@gmail.com)
# Date: June 2017

# import the OpenSeesPy compatiblity module.
import opensees.openseespy as ops

# Start of model generation
# ------------------------------

# Create a Model (with two-dimensions and 2 DOF/node)
model = ops.Model(ndm=2, ndf=2)

# Create nodes
model.node(1, (  0.0,  0.0))
model.node(2, (144.0,  0.0))
model.node(3, (168.0,  0.0))
model.node(4, ( 72.0, 96.0))

# set the boundary conditions - command: fix nodeID xRestrnt? yRestrnt?
model.fix(1, (1, 1))
model.fix(2, (1, 1))
model.fix(3, (1, 1))

# Define materials for truss elements
# -----------------------------------
# Create Elastic material prototype - command: uniaxialMaterial Elastic matID E
model.uniaxialMaterial("Elastic", 1, 3000.0)

# Define elements
# ---------------
# Create truss elements - command: element truss trussID node1 node2 A matID
model.element("Truss", 1, (1, 4), 10.0, 1)
model.element("Truss", 2, (2, 4),  5.0, 1)
model.element("Truss", 3, (3, 4),  5.0, 1)

# Define loads
# ------------
# Define the load at node 4 with components 100 and -50 in x and y:
load = {4: [100, -50.0]}

# Assign the load to a "Plain" load pattern and scale its load factor linearly in time.
model.pattern("Plain", 1, "Linear", load=load)


# ------------------------------
# Start of analysis generation
# ------------------------------

model.constraints("Plain")

# create the solution algorithm
model.algorithm("Linear")

# create the integration scheme, the LoadControl scheme using steps of 1.0
model.integrator("LoadControl", 1.0)

model.analysis("Static")


# ------------------------------
# Optionally record results
# ------------------------------
if False:
    # create a Recorder object for the nodal displacements at node 4
    model.recorder("Node",  "disp", "-file", "example.out", "-time", "-node", 4, "-dof", 1, 2)

    # create a recorder for element forces, one in global and the other local system
    model.recorder("Element", "forces", "-file", "eleGlobal.out", "-time", "-ele", 1, 2, 3)
    model.recorder("Element", "basicForces", "-file", "eleLocal.out", "-time", "-ele", 1, 2, 3)


# ------------------------------
# Finally perform the analysis
# ------------------------------

model.analyze(1)


# ------------------------------
# Print results to screen
# ------------------------------

# print the current state at node 4 and at all elements
# print("node 4 displacement: ", nodeDisp(4))
model.print(node=4)
model.print("ele")

