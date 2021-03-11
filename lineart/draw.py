from lineart import style
from lineart import transform
from flat import document

import numpy as np


def draw_edges(
    edges,
    image_size=100,
    v=False,
    background=style.canvas_fill,
    edge_style=style.blue_edge,
):

    edges = edges.reshape(-1, 2, 3)[:, :, :-1]
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


def draw_zsampled_edges(
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
    line_points = [transform.z_blur_sample_line(*e, n, scatter) for e in edges]
    points = np.concatenate(line_points)

    for p in points:
        page.place(point_style.circle(*p[:2], 0.1))
    return page.image(kind="rgba", ppi=60)
