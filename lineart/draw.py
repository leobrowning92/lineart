from lineart import style
from lineart import transform
from flat import document

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


def setup_tiled_page(
    tile_size=(100, 100), n_cols=1, n_rows=1, background=style.canvas_fill
):
    x_dim = tile_size[0] * n_cols
    y_dim = tile_size[1] * n_rows
    d = document(x_dim, y_dim, "mm")

    page = d.addpage()
    page.place(
        background.rectangle(
            0,
            0,
            x_dim,
            y_dim,
        )
    )
    return page


def draw_edges_on_tile(
    edges, col, row, tile_size, page, edge_style=style.blue_edge, v=False
):
    x_origin = col * tile_size
    y_origin = row * tile_size
    edges = edges[:, :, :-1] + np.array([x_origin, y_origin])
    for e in edges:
        page.place(edge_style.line(*e.flatten()))
    if v:
        for p in edges.reshape(-1, 2):
            page.place(style.debug.circle(*p, 2))
    return page


def draw_zsampled_edges_on_tile(
    edges,
    col,
    row,
    tile_size,
    page,
    n=1000,
    scatter=0.02,
    sand_size=0.01,
    point_style=style.blue_sand,
    v=False,
):
    x_origin = col * tile_size
    y_origin = row * tile_size
    edges = edges + np.array([x_origin, y_origin, 0])
    line_points = [z_blur_sample_line(*e, n, scatter) for e in edges]
    points = np.concatenate(line_points)

    for p in points:
        page.place(point_style.circle(*p[:2], sand_size))

    return page


def quick_draw_edges(
    edges,
    image_size=100,
    v=False,
    background=style.canvas_fill,
    edge_style=style.blue_edge,
):

    edges = edges[:, :, :-1]
    # page setup
    d = document(image_size, image_size, "mm")
    page = d.addpage()
    page.place(background.rectangle(0, 0, image_size, image_size))
    for e in edges:
        page.place(edge_style.line(*e.flatten()))
    if v:
        for p in edges.reshape(-1, 2):
            page.place(style.debug.circle(*p, 2))

    return page.image(kind="rgba", ppi=60)


def quick_draw_zsampled_edges(
    edges,
    n=1000,
    scatter=0.02,
    image_size=100,
    v=False,
    background=style.canvas_fill,
    point_style=style.blue_sand,
):

    image_size = 100
    # page setup
    d = document(image_size, image_size, "mm")
    page = d.addpage()
    page.place(background.rectangle(0, 0, image_size, image_size))
    line_points = [z_blur_sample_line(*e, n, scatter) for e in edges]
    points = np.concatenate(line_points)

    for p in points:
        page.place(point_style.circle(*p[:2], 0.1))
    return page.image(kind="rgba", ppi=60)
