from flat import rgba, shape

# colors
canvas = rgba(254, 250, 239, 255)
sand = rgba(254, 250, 219, 50)
blue = rgba(33, 80, 98, 255)
blue_low_alpha = rgba(33, 80, 98, 50)
red = rgba(255, 0, 0, 255)

# styles
blue_fill = shape().fill(blue).nostroke()
canvas_fill = shape().fill(canvas).nostroke()


canvas_edge = shape().stroke(canvas).width(1)
blue_edge = shape().stroke(blue).width(1)
blue_sand = shape().fill(blue_low_alpha).nostroke()
sand = shape().fill(sand).nostroke()
debug = shape().stroke(red).width(0.5)
full_red = shape().fill(red).nostroke()
