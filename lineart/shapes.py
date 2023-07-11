import numpy as np
from lineart.primatives import EdgeCollection


def unit_cube():
    nodes = np.array(
        [
            # xy plane nodes
            [0, 0, 0],
            [0, 1, 0],
            [1, 1, 0],
            [1, 0, 0],
            # xy plane square z+1
            [0, 0, 1],
            [0, 1, 1],
            [1, 1, 1],
            [1, 0, 1],
        ]
    )
    edges = np.array(
        [
            # xy plane square
            [nodes[0], nodes[1]],
            [nodes[1], nodes[2]],
            [nodes[2], nodes[3]],
            [nodes[3], nodes[0]],
            # xy plane square z+1
            [nodes[4], nodes[5]],
            [nodes[5], nodes[6]],
            [nodes[6], nodes[7]],
            [nodes[7], nodes[4]],
            # connection betwen z=0 and z=1 square
            [nodes[0], nodes[4]],
            [nodes[1], nodes[5]],
            [nodes[2], nodes[6]],
            [nodes[3], nodes[7]],
        ]
    )
    return EdgeCollection(edges)


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
