import numpy as np


def z_blur_sample_line(p1, p2, n, scale):
    points = sample_line(p1, p2, n)
    points = add_z_jitter(points, scale=scale)
    return points


def sample_line(p1, p2, n):
    vector = p2 - p1
    r_sample = np.random.rand(n, 1)
    points = np.multiply(r_sample, vector) + p1
    return points


def add_z_jitter(points: np.array, scale):
    n = len(points)
    z_values = points[:, 2]
    jitter_scalar = np.multiply(scale, z_values)

    jitter = np.multiply(
        (np.random.randn(n, 2) * 2 - 1),
        np.stack((jitter_scalar, jitter_scalar), axis=1),
    )
    points = points + np.concatenate(
        (jitter, np.zeros_like(z_values).reshape(-1, 1)), axis=1
    )
    return points


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
    return np.concatenate([rotation_matrix(th, normal) for th in theta]).reshape(
        -1, 3, 3
    )


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
