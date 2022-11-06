import numpy as np


class FileData:
    def __init__(self, path):
        self.path = path
        self.e_module = None
        self.area = None
        self.density = None
        self.points = np.empty((0, 2), float)
        self.elements = np.empty((0, 2), int)
        self.forces = np.array([])
        self.bc = np.array([])
        self.read_file()

    def read_file(self):
        read_points = False
        read_elements = False
        read_forces = False
        read_bc = False
        with open(self.path, "r") as f:
            text = f.readlines()
        for line in text:
            if not line.find("E="):
                self.e_module = float(line[line.find("E=") + 2:line.find(";")])
            if not line.find("Ro="):
                self.density = float(line[line.find("Ro=") + 3:line.find(";")])
            elif not line.find("A="):
                self.area = float(line[line.find("A=") + 2:line.find(";")])
            elif not line.find("Points:"):
                read_points = True
            elif not line.find("End Points;"):
                read_points = False
            elif read_points:
                point = line.split()
                point = [float(x) for x in point]
                point = np.array(point)
                self.points = np.vstack((self.points, point))
            elif not line.find("Elements:"):
                read_elements = True
            elif not line.find("End Elements;"):
                read_elements = False
            elif read_elements:
                element = line.split()
                element = [int(x) for x in element]
                element = np.array(element)
                self.elements = np.vstack((self.elements, element))
            elif not line.find("Forces:"):
                read_forces = True
            elif not line.find("End Forces;"):
                read_forces = False
            elif read_forces:
                val = line.split()
                val = [float(x) for x in val]
                self.forces = np.append(self.forces, val)
            elif not line.find("Boundary conditions:"):
                read_bc = True
            elif not line.find("End Boundary conditions:"):
                read_bc = False
            elif read_bc:
                val = line.split()
                val = [int(x) for x in val]
                self.bc = np.append(self.bc, val)


