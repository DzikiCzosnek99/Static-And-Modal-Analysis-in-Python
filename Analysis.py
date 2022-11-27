import numpy as np
from numpy.linalg import inv, eig
from Element import Element
from Point import Point


class Analysis:
    def __init__(self, file_data):
        self.file_data = file_data
        self.k = np.zeros((2 * len(file_data.points), 2 * len(file_data.points)))
        self.points = []
        self.elements = []
        self.bc = None
        self.create_bc_matrix()
        self.create_global_k_matrix()

    def create_bc_matrix(self):
        self.bc = np.matrix(self.file_data.bc)
        self.bc = self.bc.T
        self.bc = np.array(self.bc)

    def set_bc_to_matrix(self, matrix):
        output = matrix * self.bc
        output = output.transpose()
        output = output * self.bc
        output = output.transpose()
        for n in range(0, len(output[0])):
            if output[n, n] == 0:
                output[n, n] = 1
        return output

    def create_global_k_matrix(self):
        n = 1
        for p in self.file_data.points:
            self.points.append(Point(p[0], p[1], n))
            n = n + 1
        for e in self.file_data.elements:
            self.elements.append(
                Element(self.points[e[0] - 1], self.points[e[1] - 1], self.file_data.e_module, self.file_data.area,
                        len(self.points), self.file_data.density))
        for e in self.elements:
            self.k = np.add(self.k, e.global_k)


class Static(Analysis):
    def __init__(self, file_data):
        super().__init__(file_data)
        self.deformation = None
        self.calc_deformation()

    def calc_deformation(self):
        p = np.matrix([self.file_data.forces])
        new_k = self.set_bc_to_matrix(self.k)
        self.deformation = inv(new_k).dot(p.T)


class Modal(Analysis):
    def __init__(self, file_data):
        super().__init__(file_data)
        self.m = np.zeros((2 * len(file_data.points), 2 * len(file_data.points)))
        self.create_global_m_matrix()
        self.frequency = None
        self.modes = None
        self.calc_modes()

    def create_global_m_matrix(self):
        for e in self.elements:
            self.m = np.add(self.m, e.global_m)

    def calc_modes(self):
        new_k = self.set_bc_to_matrix(self.k)
        new_m = self.set_bc_to_matrix(self.m)
        self.frequency, self.modes = eig(inv(new_m).dot(new_k))
        self.modes = np.matrix(self.modes)
        new_modes = np.empty([len(self.frequency), 1])
        for n in range(0, len(self.frequency)):
            if self.frequency[n] != 1:
                new_modes = np.append(new_modes, self.modes[:, n], axis=1)
        new_modes = np.delete(new_modes, 0, axis=1)
        self.modes = new_modes
        self.frequency = [np.sqrt(x) / (2 * np.pi) for x in self.frequency if x != 1]

        for n in range(0, len(self.frequency)):
            for k in range(0, len(self.frequency)):
                if n != k and self.frequency[k] > self.frequency[n]:
                    b1 = self.frequency[k]
                    b2 = np.matrix(self.modes[:, k])
                    self.frequency[k] = self.frequency[n]
                    self.frequency[n] = b1
                    self.modes[:, k] = self.modes[:, n]
                    self.modes[:, n] = b2




