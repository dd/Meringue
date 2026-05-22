from pathlib import Path

from django.template import Library

from meringue.thumbnail.shortcuts import get_thumbnail


register = Library()


@register.filter
def thumbnail(filename, args=""):
    """
    Image processing filter. Applied to an image file path; expects comma-separated
    processing parameters as arguments. Actions are executed in the order they are specified.

    For example:

    * `s:600x400,resize,s:400x400,crop` — first sets the target size to 600x400,
      then resizes the image to that size, then sets a new target size of 400x400,
      and finally crops the canvas to 400x400.
    * `crop,s:400x400` — produces no result because the new size is specified after
      the crop action (swapping the order would crop the image to a 400x400 square).

    Filter arguments:

    * `s:<width>x<height>` — sets the target size for subsequent actions.
    * `maxw:<width>` — sets the maximum width.
    * `maxh:<height>` — sets the maximum height.
    * `crop` — changes the canvas size to the last specified target size.
    * `resize` — resizes the image to the last specified target size.
    * `c:<color>` — background fill color for crop in RGBA format (e.g., `c:255 255 255 255`).
    * `cm:left|center|right top|bottom` — crop anchor point.
    * `rm:cover|contain|stretch` — resize method.
    * `rs:no_increase|standard|no_reduce` — resize strategy.
    """

    job_chain = args.split(",")
    return get_thumbnail(file_path=Path(filename), job_chain=job_chain)
