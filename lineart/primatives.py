from lineart import transform
import numpy as np


class EdgeCollection:
    def __init__(self, edges, velocities=None, angular_velocities=None):
        self.n = edges.shape[0]
        self.edges = edges
        
        self.centers = self.edges.sum(axis=1) / 2
        self.velocities = velocities
        self.angular_velocities = angular_velocities

    def step(self, t):
        self.edges = self.edges + t * np.repeat(
            self.velocities[:, np.newaxis, :], 2, axis=1
        )
        self.rotation_step(t)
        return self

    def rotation_step(self, t):
        rot_mat = transform.multi_rot_mat(self.angular_velocities, [0, 0, 1])
        print(f"{rot_mat.shape=}")
        edge_centers = np.repeat(self.centers[:, np.newaxis, :], 2, axis=1)
        print(f"{edge_centers.shape=}")
        centers_shifted = self.edges - edge_centers
        print(f"{centers_shifted.shape=}")
        rotated = np.matmul(centers_shifted, rot_mat)
        print(f"{rotated.shape=}")
        back_shifted = rotated + edge_centers
        print(f"{back_shifted.shape=}")
        self.edges = back_shifted
        return self

    def rotate_all(self, theta, normal=[0, 0, 1]):
        """Rotate all edges about centers by an angle theta
        """
        self.edges = transform.rotate_edges(self.edges, self.centers, theta, normal)
        return self

    def rotate_unison(self, p0, normal, theta):
        """Rotate all edges about a fixed point
        """
        self.edges = transform.rotate_edges(self.edges, p0, theta, normal)
