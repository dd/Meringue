import logging
import os
from pathlib import PurePath

from rest_framework.fields import ImageField

from meringue.thumbnail.constants import FORMATS_BY_EXTENSIONS
from meringue.thumbnail.generators import DefaultThumbnailer
from meringue.thumbnail.shortcuts import _dummyimage


logger = logging.getLogger("meringue.thumbnail")


def get_format_from_path(path):
    return FORMATS_BY_EXTENSIONS[PurePath(path).suffix.lower()]


class BaseImageField(ImageField):
    def __init__(self, size=None, job_chain=None, **kwargs):
        if bool(size) and bool(job_chain):
            msg = "Need to set `size` or `job_chain` attribute (not both)."
            raise Exception(msg)

        elif size:
            self.job_chain = [
                f"s:{size[0]}x{size[1]}",
                "rm:cover",
                "rs:no_increase",
                "resize",
            ]

        elif job_chain:
            self.job_chain = job_chain

        else:
            self.job_chain = []

        super().__init__(**kwargs)


class MImageField(BaseImageField):
    """
    Optimize image to represent them
    """

    def to_representation(self, value):
        """
        TODO:
            * Add params to get_image for optimize images
        """

        if not value:
            return None

        if os.path.isfile(value.path):
            thumbnail = DefaultThumbnailer(value.path, job_chain=self.job_chain)
            optimized_image_url = thumbnail.get_image(get_format_from_path(value.path)).url
            result = optimized_image_url

        else:
            logger.error(f"File `{value.path}` not found")
            result = _dummyimage([])

        return result


class MImageSetField(ImageField):
    """
    Image field - make multiple files in different formats.

    Can set size (eg '100x100'), job_chain (arrays of jobs by dimensions) or nothing to optimize
    images only
    """

    def __init__(
        self,
        size=None,
        dimensions=None,
        base_job_chain=None,
        job_chains=None,
        **kwargs,
    ):
        if bool(size and dimensions) and bool(job_chains):
            msg = "Need to set `size` and `dimensions` or `job_chains` attribute (not both)."
            raise Exception(msg)

        elif size:
            self.job_chains = {}

            if 1 not in dimensions:
                dimensions.insert(0, 1)

            for dimension in dimensions:
                self.job_chains[dimension] = [
                    f"s:{round(size[0]*dimension)}x{round(size[1]*dimension)}",
                    *(base_job_chain or ["rm:cover", "resize", "crop"]),
                ]

        elif job_chains:
            self.job_chains = job_chains

        else:
            self.job_chains = {}

        self.spactacular_annotate()
        super().__init__(**kwargs)

    def spactacular_annotate(self):
        items = {
            "type": "object",
            "properties": {
                "srcset": {
                    "type": "string",
                    "example": (
                        "https://www.fillmurray.com/256/256 1x, "
                        "https://www.fillmurray.com/512/512 2x",
                    ),
                },
                "type": {
                    "title": "Image MIME type",
                    "type": "string",
                    "format": "MIME",
                    "example": "image/webp",
                },
            },
        }

        self._spectacular_annotation = {
            "field": {
                "type": "array",
                "items": items,
            },
            "field_component_name": None,
        }

    def to_representation(self, value):
        """
        Creates multiple images. Image with format as original image and webp.

        TODO:
            * Add params to get_image for optimize images
            * In future make av1 image
            * Check enabled webp
        """

        if not value:
            return None

        if not os.path.isfile(value.path):
            logger.error(f"File `{value.path}` not found")
            return [
                {
                    "url": _dummyimage(self.job_chains[1]),
                    "type": "image/png",
                },
            ]

        original_format = get_format_from_path(value.path)
        result = []

        for dimension, job_chain in self.job_chains.items():
            thumbnail = DefaultThumbnailer(value.path, job_chain=job_chain)
            original = thumbnail.get_image(original_format)
            webp_thumbnail = thumbnail.get_image("WEBP")

            if dimension == 1:
                result = [
                    {"srcset": f"{webp_thumbnail.url} 1x", "type": webp_thumbnail.mimetype},
                    {"srcset": f"{original.url} 1x", "type": original.mimetype},
                ]

            else:
                result[0]["srcset"] = f"{result[0]['srcset']}, {webp_thumbnail.url} {dimension}x"
                result[1]["srcset"] = f"{result[1]['srcset']}, {original.url} {dimension}x"

        return result
