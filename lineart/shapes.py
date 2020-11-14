import numpy as np
from lineart.transforms import rotate, z_blur_sample_line


class Octahedron:
    def __init__(self, center, radius):
        origin_nodes = np.array(
            [
                [0, radius, 0],
                [-radius, 0, 0],
                [0, 0, -radius],
                [radius, 0, 0],
                [0, 0, radius],
                [0, -radius, 0],
            ]
        )
        self.nodes = origin_nodes + center
        self.edges = self.edges_from_nodes()

    def edges_from_nodes(self):
        edges = np.array(
            [
                [self.nodes[0], self.nodes[1]],
                [self.nodes[0], self.nodes[2]],
                [self.nodes[0], self.nodes[3]],
                [self.nodes[0], self.nodes[4]],
                [self.nodes[5], self.nodes[1]],
                [self.nodes[5], self.nodes[2]],
                [self.nodes[5], self.nodes[3]],
                [self.nodes[5], self.nodes[4]],
                [self.nodes[1], self.nodes[2]],
                [self.nodes[2], self.nodes[3]],
                [self.nodes[3], self.nodes[4]],
                [self.nodes[4], self.nodes[1]],
            ]
        )
        return edges

    def rotate(self, p0, normal, theta):
        self.nodes = rotate(self.nodes, p0, normal, theta)
        self.edges = rotate(self.edges, p0, normal, theta)

    def sample(self, n, dither):
        line_points = [z_blur_sample_line(*e, n, dither) for e in self.edges]
        points = np.concatenate(line_points)
        return points
