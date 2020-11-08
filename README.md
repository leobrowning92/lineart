# lineart
Results of my first play around rendering images using random sampling:

![](images/2020-04-27_slow.gif)

And my first aesthetic mistake:

![](images/2020-04-27_overlap.png)

## Example

first 

    poetry install

    poetry shell

then run

    python example.py

then 

    convert -delay 20 -loop 0 outputs/*.png  output.gif

to convert the images into a gif.

## Credit:

All actual image generation done using the lovely and lightweight [Flat](https://xxyxyz.org/flat) by Xxyxyz.

Heavily inspired by the work of Anders Hoff at [Inconvergent](https://inconvergent.net/)

