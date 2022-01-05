import dask
import numpy as np
from flat import document, shape, rgba
from lineart.shapes import Octahedron
from lineart import draw


# Colors and Styles
sand = rgba(254, 250, 219, 50)
sandstyle = shape().fill(sand).nostroke()

blue = rgba(33, 80, 98, 255)
background = shape().fill(blue).nostroke()


@dask.delayed
def rotating_sampled_octagon(step, total_steps=20):
    image_size = 100
    # page setup
    d = document(image_size, image_size, "mm")
    page = d.addpage()
    page.place(background.rectangle(0, 0, image_size, image_size))
    o = Octahedron(np.array([50, 50, 40]), 40)

    o.rotate_unison(
        np.array([[50, 50, 40]]), np.array([1, 1, 1]), np.pi * 2 / total_steps * step
    )
    image = draw.draw_zsampled_edges(o.edges, n=1000, scatter=0.01)
    return image


if __name__ == "__main__":

    rotation_steps = 20

    samples = [
        rotating_sampled_octagon(i, rotation_steps).png(f"outputs/{i:03d}.png")
        for i in range(rotation_steps)
    ]

    dask.persist(*samples, scheduler="processes")
