# Meringue Thumbnail

This package provides functionality for generating image thumbnails. It supports resizing, cropping, format conversion, and various processing strategies based on a chain of jobs (commands).

The main functionality is based on the [Thumbnailer][meringue.thumbnail.generators.Thumbnailer] class, which processes images using a configurable job chain — a sequence of properties and actions applied to an image.


## Concept

The job chain is a list of string commands that are executed sequentially. Commands are divided into two types:

* **Properties** — set parameters for subsequent actions (e.g., target size, resize method). Properties are written in the format `key:value`.
* **Actions** — perform image transformations (e.g., resize, crop). Actions are written as a single word.

The order of commands matters: properties must be set before the actions that use them. The order of actions is also important — for example, `resize` followed by `crop` will first scale the image and then trim the canvas, while `crop` followed by `resize` will first trim and then scale, producing different results.


## Available properties

* `s:<width>x<height>` — sets the target size for subsequent actions. If one dimension is omitted (e.g., `s:400x`), it will be calculated proportionally.
* `maxw:<width>` — sets the maximum width.
* `maxh:<height>` — sets the maximum height.
* `c:<r> <g> <b> <a>` — background color for cropping in RGBA format (e.g., `c:255 255 255 255`).
* `cm:<horizontal> <vertical>` — crop anchor point. Horizontal: `left`, `center`, `right`. Vertical: `top`, `center`, `bottom`. Single value `center` is also accepted.
* `rm:<method>` — resize method: `cover` (fill the target area), `contain` (fit within the target area), `stretch` (stretch to exact size).
* `rs:<strategy>` — resize strategy: `standard`, `no_increase` (do not upscale), `no_reduce` (do not downscale).


## Available actions

* `resize` — resizes the image according to the current target size and resize method/strategy.
* `crop` — crops or extends the canvas to the current target size, positioning the image according to the crop method.


## Supported formats

The following image formats are supported: BMP, EPS, GIF, ICO, JPEG, PNG, TIFF, WEBP.


## Setup

Add `meringue.thumbnail` to `INSTALLED_APPS`:

```python title="settings.py"
INSTALLED_APPS = (
    ...
    "meringue.thumbnail",
    ...
)
```

The package requires [Pillow](https://python-pillow.org/) for image processing:

```console
$ pip install Pillow
```


## Usage


### Shortcut

The simplest way to generate a thumbnail is using the [get_thumbnail][meringue.thumbnail.shortcuts.get_thumbnail] shortcut:

```python
from pathlib import Path
from meringue.thumbnail.shortcuts import get_thumbnail

url = get_thumbnail(
    file_path=Path("/path/to/image.jpg"),
    job_chain=["s:300x200", "rm:cover", "resize", "crop"],
    out_format="WEBP",
)
```

If the source file does not exist, a dummy image URL will be returned.


### Thumbnailer

For more control, you can use the [Thumbnailer][meringue.thumbnail.generators.Thumbnailer] directly:

```python
from pathlib import Path
from meringue.thumbnail.generators import DefaultThumbnailer

thumbnailer = DefaultThumbnailer(
    image_path=Path("/absolute/path/to/image.jpg"),
    job_chain=["s:600x400", "resize", "s:400x400", "crop"],
)
thumbnail = thumbnailer.get_thumbnail("WEBP")
print(thumbnail.url)
```

!!! note
	The `image_path` must be an absolute path.


### Templatetags


#### thumbnail

::: meringue.thumbnail.templatetags.m_thumbnails.thumbnail
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false

```html
{% load m_thumbnails %}

<img src="{{ image_path|thumbnail:'s:300x200,rm:cover,resize,crop' }}" />
```


### DRF fields

For the Django REST Framework, the package provides two serializer fields:


#### MImageField

[MImageField][meringue.thumbnail.drf_fields.MImageField] — a field that returns a URL to an optimized image. You can specify either `size` or `job_chain`:

```python
from meringue.thumbnail.drf_fields import MImageField

class MySerializer(serializers.ModelSerializer):
    photo = MImageField(size=(300, 200))
    # or
    photo = MImageField(job_chain=["s:300x200", "rm:cover", "rs:no_increase", "resize"])
```


#### MImageSetField

[MImageSetField][meringue.thumbnail.drf_fields.MImageSetField] — a field that returns a set of images in different formats (original + WebP) and dimensions (1x, 2x, etc.) for use with the `<picture>` element. Under the hood, the image is processed once per dimension and then saved into multiple formats, which saves resources compared to running the full job chain separately for each format:

```python
from meringue.thumbnail.drf_fields import MImageSetField

class MySerializer(serializers.ModelSerializer):
    photo = MImageSetField(size=(300, 200), dimensions=(1, 2))
```

The response will contain an array of objects with `srcset` and `type` fields:

```json
[
	{"srcset": "/media/m/thumbnail/.../image.webp 1x, .../image.webp 2x", "type": "image/webp"},
	{"srcset": "/media/m/thumbnail/.../image.jpg 1x, .../image.jpg 2x", "type": "image/jpeg"}
]
```


## Storage

Thumbnails are saved to a separate storage configured via [THUMBNAIL_DIR][meringue.conf.default_settings.THUMBNAIL_DIR] and [THUMBNAIL_URL][meringue.conf.default_settings.THUMBNAIL_URL]. The storage initialization can be customized through the [THUMBNAIL_STORAGE_GETTER][meringue.conf.default_settings.THUMBNAIL_STORAGE_GETTER] setting.


## Image optimization

The [THUMBNAIL_IMAGE_OPTIMIZE_HANDLER][meringue.conf.default_settings.THUMBNAIL_IMAGE_OPTIMIZE_HANDLER] setting can be used to optimize the generated image before it is saved to thumbnail storage. The handler receives the [ThumbnailImage][meringue.thumbnail.images.ThumbnailImage] instance and an in-memory image file. It must return an in-memory image file.

```python title="settings.py"
MERINGUE = {
    "THUMBNAIL_IMAGE_OPTIMIZE_HANDLER": "project.thumbnails.optimize_thumbnail",
}
```

```python title="project/thumbnails.py"
from io import BytesIO


def optimize_thumbnail(thumbnail_image, image_file):
    image_file.seek(0)
    image_data = image_file.read()

    optimized_data = optimize_image(image_data, thumbnail_image.out_format)

    return BytesIO(optimized_data)
```

If the image should not be changed, return the original `image_file`.

By default, [THUMBNAIL_IMAGE_OPTIMIZE_HANDLER][meringue.conf.default_settings.THUMBNAIL_IMAGE_OPTIMIZE_HANDLER] uses the built-in [optimize][meringue.thumbnail.optimizers.optimize] handler. Built-in optimizers are configured through [THUMBNAIL_OPTIMIZERS][meringue.conf.default_settings.THUMBNAIL_OPTIMIZERS]. The default value is an empty dictionary, so no external optimizer is executed until it is explicitly configured.

Currently, the built-in handler supports `oxipng` for PNG files. The optimizer reads the generated thumbnail from memory and returns an optimized in-memory file before it is saved to storage:

```python title="settings.py"
MERINGUE = {
    "THUMBNAIL_OPTIMIZERS": {
        "oxipng": {
            "binary": "oxipng",
        },
    },
}
```

You can override oxipng command-line options:

```python title="settings.py"
MERINGUE = {
    "THUMBNAIL_OPTIMIZERS": {
        "oxipng": {
            "binary": "/usr/bin/oxipng",
            "options": "-o 4 --strip all",
        },
    },
}
```

The `options` value can also be a list of strings if you prefer to pass already-split command-line arguments.


## Customization

The thumbnail system is highly customizable through settings:

* [THUMBNAIL_GENERATOR_CLASS][meringue.conf.default_settings.THUMBNAIL_GENERATOR_CLASS] — custom thumbnailer class.
* [THUMBNAIL_IMAGE_CLASS][meringue.conf.default_settings.THUMBNAIL_IMAGE_CLASS] — custom thumbnail image class.
* [THUMBNAIL_PROPERTIES][meringue.conf.default_settings.THUMBNAIL_PROPERTIES] — register custom properties.
* [THUMBNAIL_ACTIONS][meringue.conf.default_settings.THUMBNAIL_ACTIONS] — register custom actions.
* [THUMBNAIL_DEFAULT_FORMAT][meringue.conf.default_settings.THUMBNAIL_DEFAULT_FORMAT] — default output format (default: PNG).
* [THUMBNAIL_DEFAULT_CROP_METHOD][meringue.conf.default_settings.THUMBNAIL_DEFAULT_CROP_METHOD] — default crop method.
* [THUMBNAIL_DEFAULT_RESIZE_METHOD][meringue.conf.default_settings.THUMBNAIL_DEFAULT_RESIZE_METHOD] — default resize method (default: contain).
* [THUMBNAIL_DEFAULT_RESIZE_STRATEGY][meringue.conf.default_settings.THUMBNAIL_DEFAULT_RESIZE_STRATEGY] — default resize strategy (default: standard).
* [THUMBNAIL_DEFAULT_BG_COLOR][meringue.conf.default_settings.THUMBNAIL_DEFAULT_BG_COLOR] — default background color.
* [THUMBNAIL_SAVE_PARAMS_BY_FORMAT][meringue.conf.default_settings.THUMBNAIL_SAVE_PARAMS_BY_FORMAT] — format-specific save parameters (e.g., JPEG quality).
* [THUMBNAIL_IMAGE_OPTIMIZE_HANDLER][meringue.conf.default_settings.THUMBNAIL_IMAGE_OPTIMIZE_HANDLER] — in-memory optimization hook called before saving thumbnail to storage. It must return an in-memory image file.
* [THUMBNAIL_OPTIMIZERS][meringue.conf.default_settings.THUMBNAIL_OPTIMIZERS] — built-in thumbnail optimizer settings.
* [THUMBNAIL_DUMMYIMAGE_TEMPLATE][meringue.conf.default_settings.THUMBNAIL_DUMMYIMAGE_TEMPLATE] — template for dummy image URL when source file is not found.
