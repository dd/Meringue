import copy
import logging
from pathlib import Path
from typing import Any
from typing import Final

from django.core.files.storage import Storage
from django.utils.functional import lazy

from PIL import Image

from meringue.conf import m_settings
from meringue.thumbnail import constants
from meringue.thumbnail.exceptions import WrongActionOrPropertyError
from meringue.thumbnail.exceptions import WrongFormatError
from meringue.thumbnail.images import DefaultThumbnailImage
from meringue.thumbnail.storage import default_storage
from meringue.thumbnail.types import JobChainType


logger = logging.getLogger("meringue.thumbnail")


DEFAULT_OPTIONS: Final[dict[str, Any]] = {
    constants.PROP_BG_COLOR: m_settings.THUMBNAIL_DEFAULT_BG_COLOR,
    constants.PROP_CROP_METHOD: m_settings.THUMBNAIL_DEFAULT_CROP_METHOD,
    constants.PROP_MAX_HEIGHT: None,
    constants.PROP_MAX_WIDTH: None,
    constants.PROP_RESIZE_METHOD: m_settings.THUMBNAIL_DEFAULT_RESIZE_METHOD,
    constants.PROP_RESIZE_STRATEGY: m_settings.THUMBNAIL_DEFAULT_RESIZE_STRATEGY,
}


class Thumbnailer:
    """
    Thumbnail generator class.

    Todo:

    * aliases for job changes
    """

    def __init__(
        self,
        image_path: Path,
        job_chain: JobChainType,
        storage: Storage | None = None,
    ):
        """
        Attributes:
            image_path: Source image path.
            job_chain: Thumbnail job chain.
            storage: File storage.
        """

        if not image_path.is_absolute():
            msg = "`image_path` must be absolute"
            raise AttributeError(msg, name="image_path")

        self.source_image_path = image_path
        self.job_chain = job_chain
        self.storage = storage or default_storage

    def make_thumbnail(self) -> Image:
        """
        Makes a thumbnail based on a quest chain.

        Raises:
            WrongActionOrPropertyError: Invalid action or property.

        Returns:
            Pillow image.
        """

        logger.debug(f"Thumbnail is made using job chain: {', '.join(self.job_chain)}")

        # openingn and prepearing file
        image = Image.open(self.source_image_path)
        image = image.convert("RGBA")

        # prepearing options
        options = copy.deepcopy(DEFAULT_OPTIONS)
        options[constants.PROP_CURRENT_SIZE] = [float(i) for i in image.size]
        options[constants.PROP_NEW_SIZE] = options[constants.PROP_CURRENT_SIZE].copy()

        # applying modifiers
        for job in self.job_chain:
            if ":" in job:
                # property
                prop, args = job.split(":")
                options.update(m_settings.THUMBNAIL_PROPERTIES[prop](args, options))

            elif job in m_settings.THUMBNAIL_ACTIONS:
                # action
                image = m_settings.THUMBNAIL_ACTIONS[job](image, options)

            else:
                raise WrongActionOrPropertyError(job)

        return image

    def get_thumbnail(self, out_format: str, **kwargs) -> DefaultThumbnailImage:
        """
        Generates and returns a preview image in the specified format.

        Attributes:
            out_format: Output image format.
            **kwargs: Output image save extra params.

        Raises:
            WrongFormatError: Format is not supported.

        Returns:
            Thumbnail image.
        """

        if out_format not in constants.EXTENSIONS_BY_FORMATS:
            raise WrongFormatError(out_format)

        image = lazy(self.make_thumbnail, Image.Image)()
        thumbnail_image = DefaultThumbnailImage(
            image_path=self.source_image_path,
            job_chain=self.job_chain,
            out_format=out_format,
            image=image,
            storage=self.storage,
        )
        thumbnail_image.save(**kwargs)

        return thumbnail_image


DefaultThumbnailer: Final = m_settings.THUMBNAIL_GENERATOR_CLASS
