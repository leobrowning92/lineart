import numpy as np
from lineart.primatives import EdgeCollection


def octahedron(center, radius):
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
    nodes = origin_nodes + center
    edges = np.array(
        [
            [nodes[0], nodes[1]],
            [nodes[0], nodes[2]],
            [nodes[0], nodes[3]],
            [nodes[0], nodes[4]],
            [nodes[5], nodes[1]],
            [nodes[5], nodes[2]],
            [nodes[5], nodes[3]],
            [nodes[5], nodes[4]],
            [nodes[1], nodes[2]],
            [nodes[2], nodes[3]],
            [nodes[3], nodes[4]],
            [nodes[4], nodes[1]],
        ]
    )
    return EdgeCollection(edges)
