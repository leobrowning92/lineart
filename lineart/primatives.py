from lineart import transform
import numpy as np
import logging

logger = logging.getLogger(__name__)


class EdgeCollection:
    def __init__(self, edges, velocities=None, angular_velocities=None):
        self.n = edges.shape[0]
        self.edges = edges

        self.lengths = self.calc_lengths()
        if velocities is None:
            self.velocities = np.zeros(edges[:, 0, :].shape)
        else:
            self.velocities = velocities
        if angular_velocities is None:
            # default is very small numbers to avoid zeros for rotation
            self.angular_velocities = np.ones(edges[:, 0, :].shape) / 1e10
        else:
            self.angular_velocities = angular_velocities

    @property
    def centers(self):
        return self.edges.sum(axis=1) / 2

    def calc_lengths(self):
        diffs = self.edges[:, 1, :] - self.edges[:, 0, :]
        return np.linalg.norm(diffs, axis=1)

    def step(self, t):
        self.edges = self.edges + t * np.repeat(
            self.velocities[:, np.newaxis, :], 2, axis=1
        )
        self.rotation_step(t)
        return self

    def rotation_step(self, t):

        angle = t * np.linalg.norm(self.angular_velocities, axis=1)
        rot_mat = transform.multi_rot_mat(angle, self.angular_velocities)
        logger.debug(f"{rot_mat.shape=}")
        edge_centers = np.repeat(self.centers[:, np.newaxis, :], 2, axis=1)
        logger.debug(f"{edge_centers.shape=}")
        centers_shifted = self.edges - edge_centers
        logger.debug(f"{centers_shifted.shape=}")
        rotated = np.matmul(centers_shifted, rot_mat)
        logger.debug(f"{rotated.shape=}")
        back_shifted = rotated + edge_centers
        logger.debug(f"{back_shifted.shape=}")
        self.edges = back_shifted
        return self

    def rotate_all(self, theta, normal=[0, 0, 1]):
        """Rotate all edges about centers by an angle theta"""
        self.edges = transform.rotate_edges(self.edges, self.centers, theta, normal)
        return self

    def rotate_unison(self, p0, normal, theta):
        """Rotate all edges about a fixed point"""
        self.edges = transform.rotate_edges(self.edges, p0, theta, normal)
        return self

    def copy(self):
        return EdgeCollection(
            self.edges, velocities=self.velocities, angular_velocities=self.angular_velocities
        )

    def combine(self, other):
        new_e = np.concatenate((self.edges, other.edges), axis=0)
        if self.velocities is None or other.velocities is None:
            new_v = None
        else:
            new_v = np.concatenate((self.velocities, other.velocities), axis=0)

        if self.angular_velocities is None or other.angular_velocities is None:
            new_av = None
        else:
            new_av = np.concatenate((self.angular_velocities, other.angular_velocities), axis=0)
        return EdgeCollection(new_e, velocities=new_v, angular_velocities=new_av)

    def __repr__(self):

        info = [
            f"{type(self).__name__} at: object.__repr__(self)",
            f"{self.edges.shape=}",
            f"{self.centers.mean(axis=0)=}"
            f"self.lengths (min, mean, max) : ({self.lengths.min():0.2f}, {self.lengths.mean():0.2f}, {self.lengths.max():0.2f})",
        ]
        return "\n".join(info)
