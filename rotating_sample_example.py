import dask
import numpy as np
from flat import document, shape, rgba
from lineart.shapes import Octahedron


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

    o.rotate([50, 50, 40], [1, 1, 1], np.pi * 2 / total_steps * step)
    samples = o.sample(1000, 0.02)

    for p in samples:
        page.place(sandstyle.circle(*p[:2], 0.1))
    # Display image
    page.image(kind="rgba", ppi=60).png(f"outputs/{step:03d}.png")
    return step


if __name__ == "__main__":

    rotation_steps = 4

    samples = [
        rotating_sampled_octagon(i, rotation_steps) for i in range(rotation_steps)
    ]

    dask.persist(*samples, scheduler="processes")
