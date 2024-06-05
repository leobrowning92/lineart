from flat import rgba, shape

# colors
canvas = rgba(254, 250, 239, 255)
sand = rgba(254, 250, 219, 50)
blue = rgba(33, 80, 98, 255)
blue_low_alpha = rgba(33, 80, 98, 50)
red = rgba(255, 0, 0, 255)


## wildflower colors
wildflower_greens = [
    rgba(22, 47, 9, 255),
    rgba(113, 157, 54, 255),
    rgba(27, 58, 11, 255),
    rgba(22, 47, 9, 255),
]


wildflower_reds = [
    rgba(22, 47, 9, 255),
    rgba(166, 34, 23, 255),
]


wildflower_purples = [
    rgba(166, 34, 23, 255),
    rgba(136, 52, 130, 255),
]


wildflower_golds = [
    rgba(229, 168, 60, 255),
    rgba(222, 146, 51, 255),
]

# styles
blue_fill = shape().fill(blue).nostroke()
canvas_fill = shape().fill(canvas).nostroke()


canvas_edge = shape().stroke(canvas).width(1)
blue_edge = shape().stroke(blue).width(1)
blue_sand = shape().fill(blue_low_alpha).nostroke()
sand = shape().fill(sand).nostroke()
debug = shape().stroke(red).width(0.5)
full_red = shape().fill(red).nostroke()


def simple_edge(color: rgba) -> shape:
    return shape().stroke(color).width(1)
