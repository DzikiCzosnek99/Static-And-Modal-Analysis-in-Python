import numpy as np


class Element:
    def __init__(self, point1, point2, e_module, area, el_number, density=None):
        self.point1 = point1
        self.point2 = point2
        self.length = np.sqrt(pow(point1.x_pos - point2.x_pos, 2) + pow(point1.y_pos - point2.y_pos, 2))
        self.e_module = e_module
        self.area = area
        self.density = density
        self.local_k = np.array([[1, 0, -1, 0], [0, 0, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 0]]) * \
                       (self.e_module * self.area / self.length)
        self.cos = (point2.x_pos - point1.x_pos) / self.length
        self.sin = (point2.y_pos - point1.y_pos) / self.length
        self.el_number = el_number
        self.global_k = self.local_to_global(self.local_k)
        self.local_m = None
        self.global_m = None
        if density is not None:
            self.local_m = np.array([[2, 0, 1, 0], [0, 2, 0, 1], [1, 0, 2, 0], [0, 1, 0, 2]]) * \
                       (self.density * self.area * self.length / 6)
            self.global_m = self.local_to_global(self.local_m)

    def local_to_global(self, matrix):
        dc = np.array([[self.cos, self.sin, 0, 0], [-self.sin, self.cos, 0, 0], [0, 0, self.cos, self.sin],
                       [0, 0, -self.sin, self.cos]])
        output_matrix = dc.transpose().dot(matrix).dot(dc)
        q1 = output_matrix[0:2, 0:2]
        q2 = output_matrix[2:4, 0:2]
        q3 = output_matrix[0:2, 2:4]
        q4 = output_matrix[2:4, 2:4]
        output_matrix = np.zeros((2 * self.el_number, 2 * self.el_number))
        r = 2 * self.point1.number - 2
        c = 2 * self.point1.number - 2
        output_matrix[r:r + 2, c:c + 2] = q1
        c = 2 * self.point2.number - 2
        output_matrix[r:r + 2, c:c + 2] = q2
        r = 2 * self.point2.number - 2
        c = 2 * self.point1.number - 2
        output_matrix[r:r + 2, c:c + 2] = q3
        r = 2 * self.point2.number - 2
        c = 2 * self.point2.number - 2
        output_matrix[r:r + 2, c:c + 2] = q4
        return output_matrix
