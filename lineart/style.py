from flat import rgba, shape

# colors
canvas = rgba(254, 250, 219, 255)
sand = rgba(254, 250, 219, 50)
blue = rgba(33, 80, 98, 255)
red = rgba(255, 0, 0, 255)

# styles
background = shape().fill(blue).nostroke()
edge = shape().stroke(canvas).width(1)
sand = shape().fill(sand).nostroke()
debug = shape().stroke(red).width(0.5)
