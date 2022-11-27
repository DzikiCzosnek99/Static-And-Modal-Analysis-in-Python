import matplotlib.pyplot as plt
import numpy as np


class Results:
    def __init__(self, analysis):
        self.analysis = analysis

    def plot_deformations(self, scale=1):
        n = 0
        fiq, ax = plt.subplots()
        for e in self.analysis.elements:
            x1 = e.point1.x_pos
            x2 = e.point2.x_pos
            y1 = e.point1.y_pos
            y2 = e.point2.y_pos

            dx1 = self.analysis.deformation[2 * e.point1.number - 2, 0] * scale
            dx2 = self.analysis.deformation[2 * e.point2.number - 2, 0] * scale
            dy1 = self.analysis.deformation[2 * e.point1.number - 1, 0] * scale
            dy2 = self.analysis.deformation[2 * e.point2.number - 1, 0] * scale

            if n == 0:
                l1 = "Rama nieodksztalcona"
                l2 = "Rama odksztalcona"
            else:
                l1 = None
                l2 = None

            ax.plot([x1, x2], [y1, y2], '--', color="black", linewidth=1, marker="o", markersize=3, label=l1)
            ax.plot([x1 + dx1, x2 + dx2], [y1 + dy1, y2 + dy2], color="red", linewidth=1.25, marker="o", markersize=3,
                    label=l2)
            ax.legend()
            ax.set_title(f"Wykres odksztalcen skala={scale}:1")
            ax.set_ylabel("Wspolrzedna Y [m]")
            ax.set_xlabel("Wspolrzedna X [m]")

            n = n + 1

        plt.show()

    def plot_mode_deformations(self, mode, scale=1):
        deformations = np.array(self.analysis.modes[:, mode - 1])
        deformation = [x / max(abs(deformations)) for x in deformations]
        n = 0
        fiq, ax = plt.subplots()
        for e in self.analysis.elements:
            x1 = e.point1.x_pos
            x2 = e.point2.x_pos
            y1 = e.point1.y_pos
            y2 = e.point2.y_pos

            dx1 = deformation[2 * e.point1.number - 2] * scale
            dx2 = deformation[2 * e.point2.number - 2] * scale
            dy1 = deformation[2 * e.point1.number - 1] * scale
            dy2 = deformation[2 * e.point2.number - 1] * scale

            if n == 0:
                l1 = "Rama nieodksztalcona"
                l2 = "Rama odksztalcona"
            else:
                l1 = None
                l2 = None

            ax.plot([x1, x2], [y1, y2], '--', color="black", linewidth=1, marker="o", markersize=3, label=l1)
            ax.plot([x1 + dx1, x2 + dx2], [y1 + dy1, y2 + dy2], color="red", linewidth=1.25, marker="o", markersize=3,
                    label=l2)
            ax.legend()
            ax.set_title(f"Postac drgan wnasnych dla f={round(self.analysis.frequency[mode - 1], 2)}[Hz]")
            ax.set_ylabel("Wspolrzedna Y [m]")
            ax.set_xlabel("Wspolrzedna X [m]")

            n = n + 1

        plt.show()
