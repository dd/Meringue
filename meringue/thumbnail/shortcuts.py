import logging
import re
from pathlib import Path

from django.conf import settings

from meringue.conf import m_settings
from meringue.thumbnail.generators import DefaultThumbnailer
from meringue.thumbnail.types import JobChainType


logger = logging.getLogger("meringue.thumbnail")


def _dummyimage(job_chain: str) -> str:
    """
    Return link to dummy image

    TODO:
     * configurated dummy image?

    Attributes:
        job_chain: Thumbnail job chain.

    Returns:
        Dummy image url.
    """

    if settings.DEBUG:
        size = (42, 42)
        job_chain.reverse()
        final_size = re.compile(r"s:(\d+)x(\d+)")
        for task in job_chain:
            try:
                size = final_size.search(task).groups()
                break
            except AttributeError:
                pass

        return m_settings.THUMBNAIL_DUMMYIMAGE_TEMPLATE.format(
            width=size[0],
            height=size[1],
        )

    return "%simages/noise.png" % settings.STATIC_URL
    # return "%simages/none.gif" % settings.STATIC_URL


def get_thumbnail(
    file_path: Path,
    job_chain: JobChainType,
    out_format: str = m_settings.THUMBNAIL_DEFAULT_FORMAT,
    **kwargs,
) -> str:
    """
    Shortcut to make single image preview

    Attributes:
        file_path: Source file path.
        job_chain: Thumbnail job chain.
        format: Output image format.
        **kwargs: Output image save extra params.

    Returns:
        Thumbnail url.
    """

    if not file_path.exists():
        msg = f"File `{file_path}` not found."
        logger.error(msg)
        return _dummyimage(job_chain)

    thumbnailer = DefaultThumbnailer(file_path, job_chain=job_chain)
    thumbnail_image = thumbnailer.get_thumbnail(out_format, **kwargs)
    return thumbnail_image.url
