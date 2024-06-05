from lineart import style
from flat import document
from datetime import datetime
from flat.document import page
from itertools import product
from IPython.display import Image
from typing import Tuple
from lineart.projection import EDGE_PROJECTIONS
import numpy as np
from lineart.primatives import EdgeCollection


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
    tile_size: Tuple[int, int] = (100, 100),
    n_tiles: Tuple[int, int] = (1, 1),
    gap: Tuple[int, int] = (0, 0),
    background=style.canvas_fill,
) -> page:

    # FUTURE: vectorise this code to use np arrays
    x_dim = (tile_size[0] + gap[0]) * n_tiles[0] + gap[0]
    y_dim = (tile_size[1] + gap[1]) * n_tiles[1] + gap[1]
    dim = (x_dim, y_dim)
    print(f"{dim=}")
    origins = np.empty((*n_tiles, 2))
    for i, j in product(range(n_tiles[0]), range(n_tiles[1])):
        origins[i, j] = np.array(
            [i * (tile_size[0] + gap[0]) + gap[0], j * (tile_size[1] + gap[1]) + gap[1]]
        )
    d = document(x_dim, y_dim, "mm")

    page = d.addpage()
    page.place(background.rectangle(0, 0, *dim))
    return page, origins


def draw_edges_on_tile(
    edges,
    col,
    row,
    page,
    origins,
    edge_style=style.blue_edge,
    v=False,
    projection="xy_plane",
) -> page:
    proj_edges = EDGE_PROJECTIONS[projection](edges)
    draw_edges = proj_edges + np.array([*origins[col, row]])
    for e in draw_edges:
        page.place(edge_style.line(*e.flatten()))
    if v:
        for p in draw_edges.reshape(-1, 2):
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
) -> page:
    x_origin = col * tile_size
    y_origin = row * tile_size
    edges = edges + np.array([x_origin, y_origin, 0])
    line_points = [z_blur_sample_line(*e, n, scatter) for e in edges]
    points = np.concatenate(line_points)

    for p in points:
        page.place(point_style.circle(*p[:2], sand_size))

    return page


def make_page(image_size, background=style.canvas_fill) -> page:
    # page setup
    d = document(image_size, image_size, "mm")
    page = d.addpage()
    page.place(background.rectangle(0, 0, image_size, image_size))
    return page


def quick_draw_edges(
    edges: EdgeCollection,
    image_size=100,
    v=False,
    background=style.canvas_fill,
    edge_style=style.blue_edge,
    page=None,
    unit_scale=False,
) -> page:
    # flat projection onto the xy plane
    if unit_scale:
        edges = edges * image_size
    if edges.shape[-1] == 3:
        edges = edges[:, :, :-1]
    if page is None:
        page = make_page(image_size, background)
    for e in edges:
        page.place(edge_style.line(*e.flatten()))
    if v:
        for p in edges.reshape(-1, 2):
            page.place(style.debug.circle(*p, 2))

    return page


def quick_draw_zsampled_edges(
    edges,
    n=1000,
    scatter=0.02,
    image_size=100,
    v=False,
    background=style.canvas_fill,
    point_style=style.blue_sand,
    page=None,
) -> page:

    image_size = 100
    # page setup

    if page is None:
        # page setup
        page = make_page(image_size)
    line_points = [z_blur_sample_line(*e, n, scatter) for e in edges]
    points = np.concatenate(line_points)

    for p in points:
        page.place(point_style.circle(*p[:2], 0.1))
    return page


def page_save_iteration(
    page: page, name: str = "", show=False, thumb=True, output_dir="../outputs/"
) -> Image:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # path hardcoded to be run from notebooks directory
    name = "name" if not name else name
    basename = f"{output_dir}{name}_{timestamp}"
    page.svg(f"{basename}.svg")
    if thumb:
        page.image(kind="rgba", ppi=60).png(f"{basename}_thumb.png")
    if show:
        return Image(page.image(kind="rgba", ppi=60).png())
