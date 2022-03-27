import numpy as np
import logging

logger = logging.getLogger(__name__)


def rotation_matrix(theta, normal):
    ux, uy, uz = normal / np.linalg.norm(normal)
    rot_mat = np.array(
        [
            [
                np.cos(theta) + ux ** 2 * (1 - np.cos(theta)),
                ux * uy * (1 - np.cos(theta)) - uz * np.sin(theta),
                ux * uz * (1 - np.cos(theta)) + uy * np.sin(theta),
            ],
            [
                uy * ux * (1 - np.cos(theta)) + uz * np.sin(theta),
                np.cos(theta) + uy ** 2 * (1 - np.cos(theta)),
                uy * uz * (1 - np.cos(theta)) - ux * np.sin(theta),
            ],
            [
                uz * ux * (1 - np.cos(theta)) - uy * np.sin(theta),
                uz * uy * (1 - np.cos(theta)) + ux * np.sin(theta),
                np.cos(theta) + uz ** 2 * (1 - np.cos(theta)),
            ],
        ]
    )
    return rot_mat


def multi_rot_mat(theta, normal):
    rotation_matrices = np.concatenate(
        [rotation_matrix(th, nrm) for th, nrm in zip(theta, normal)]
    )
    return rotation_matrices.reshape(-1, 3, 3)


def rotate_points(points, centers, theta, normal):
    rot_mat = rotation_matrix(theta, normal)
    centers_shifted = points - centers
    rotated = centers_shifted.dot(rot_mat)
    back_shifted = rotated + centers
    return back_shifted


def rotate_edges(edges, centers, theta, normal):
    edge_centers = np.repeat(centers[:, np.newaxis, :], 2, axis=1)
    return rotate_points(edges, edge_centers, theta, normal)


def rotate_points_xy(point, p0, theta):
    return rotate_points(point, p0, theta, [0, 0, 1])


def rand_split_edge(e, n):
    fracs = np.random.rand(n, 1)
    fracs.sort(axis=0)
    vector = e[1] - e[0]
    splits = np.multiply(fracs[::-1], vector) + e[0]
    points = np.concatenate((e[1].reshape(1, 3), splits, e[0].reshape(1, 3)))
    starts = points[:-1]
    ends = points[1:]
    edges = np.concatenate((starts.reshape(-1, 1, 3), ends.reshape(-1, 1, 3)), axis=1)
    return edges


def collection_dot(a, b):
    for v in (a, b):
        assert len(v.shape) == 2
        assert a.shape[1] == 3
    return np.sum(a * b, axis=1)


def edge_rot_push(ec, F, pf):
    cs = ec.centers
    p0s = ec.edges[:, 0, :]
    p1s = ec.edges[:, 1, :]
    dw = 0
    for ps in [ec.edges[:, 0, :], ec.edges[:, 1, :]]:
        rs = ps - cs
        ds = ps - pf
        dwi = (
            np.divide(
                np.cross(rs, ds),
                (collection_dot(ds, ds) * collection_dot(rs, rs))[:, None],
            )
            * F
        )
        dw += dwi
    return dw


def edge_vel_push(ec, F, pf):
    cs = ec.centers

    ds = cs - pf
    dv = np.divide(ds / np.linalg.norm(ds), collection_dot(ds, ds)[:, None]) * F
    return dv


def point_push(ec, F, pf):
    dv = edge_vel_push(ec, F, pf)
    dw = edge_rot_push(ec, F, pf)
    ec.velocities = ec.velocities + dv
    ec.angular_velocities = ec.angular_velocities + dw
    logger.debug(f"{dv=}\n{dw=}")
    return ec
