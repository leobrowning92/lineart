from lineart import transform
import numpy as np


class EdgeCollection:
    def __init__(self, edges, velocities):
        self.edges = edges
        self.velocities = velocities
        self.centers = self.edges.sum(axis=1) / 2

    def move(self, t):
        self.edges = self.edges + t * np.repeat(
            self.velocities[:, np.newaxis, :], 2, axis=1
        )
        return self

    def rotate_indiv(self, theta, normal=[0, 0, 1]):
        self.edges = transform.rotate_edges(self.edges, self.centers, theta, normal)
        return self
