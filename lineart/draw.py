from lineart import style
from flat import document


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

    return page.image(kind="rgba", ppi=60).png()
