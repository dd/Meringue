import hashlib
import json
import mimetypes
from io import BytesIO
from pathlib import Path
from typing import Final

from django.core.files.storage import Storage
from django.db.models.utils import AltersData

from PIL import Image

from meringue.conf import m_settings
from meringue.thumbnail import constants
from meringue.thumbnail.storage import default_storage
from meringue.thumbnail.types import JobChainType


class ThumbnailImage(AltersData):
    """
    Thumbnail Image class.
    """

    def __init__(
        self,
        image_path: Path,
        job_chain: JobChainType,  # str  = "extra@1",
        out_format: str,
        image: Image,
        storage: Storage | None = None,
    ):
        """
        Attributes:
            image_path: Source image path.
            job_chain: Thumbnail job chain.
            out_format: Output image format.
            image: Thumbnail PIL image.
            storage: File storage.
        """

        self.source_image_path = image_path
        self.job_chain = job_chain
        self.out_format = out_format
        self.image = image
        self.storage = storage or default_storage
        self._saved = None

    @property
    def name(self) -> Path:
        """
        Relative path to thumbnail.

        We split the path into separate directories so as not to dump everything in one directory,
        which can be a problem with a large count of images.

        Returns:
            Thumbnail path.
        """

        filename = self.filename
        path = Path(filename[:2], filename[2:4], filename)
        return path

    @property
    def thumbnail_hash(self) -> str:
        """
        Calculates the thumbnail hash based on the job chain and source path.

        Returns:
            Thumbnail hash.
        """

        if getattr(self, "_thumbnail_hash", None) is None:
            params = [
                self.source_image_path.as_posix(),
                json.dumps(self.job_chain),
            ]
            salt = "|".join(params)
            self._thumbnail_hash = hashlib.md5(salt.encode()).hexdigest()  # noqa: S324

        return self._thumbnail_hash

    @property
    def file_extension(self) -> str:
        """
        Returns the file extension for the thumbnail.

        Returns:
            Thumbnail file extension.
        """

        return constants.EXTENSIONS_BY_FORMATS[self.out_format]

    @property
    def filename(self) -> str:
        """
        Returns the file name for the thumbnail.

        Returns:
            Thumbnail file name.
        """

        return f"{self.thumbnail_hash}{self.file_extension}"

    @property
    def path(self) -> Path:
        """Absolute path to thumbnail."""
        return self.storage.path(self.name)

    @property
    def url(self) -> str:
        """Url to thumbnail."""
        return self.storage.url(self.name)

    @property
    def is_supports_alpha(self) -> bool:
        """Returns the alpha channel support flag."""
        return self.out_format in constants.FORMATS_WITH_ALPHA_SUPPORT

    @property
    def mimetype(self) -> str:
        """
        Return thumbnail mimetype.

        Python mimetypes library doesn't know webp =(.

        Returns:
            Thumbnail mimetype.
        """

        if self.out_format == constants.FORMAT_WEBP:
            return "image/webp"

        guess_type = mimetypes.guess_type(str(self.absolute_path))[0]
        return guess_type[0]

    @property
    def saved(self) -> bool:
        """
        Check saved on disk thumbnail or not.

        Returns:
            Saved on disk flag.
        """

        if self._saved is None:
            self._saved = Path(self.path).exists()

        return self._saved

    def save(self, force=False, **kwargs):
        """
        Save image to disk.

        Attributes:
            **kwargs: Pillow imamge save params.
        """

        if (not force) and self.saved:
            return

        image = self.image.copy()

        if not self.is_supports_alpha:
            image = image.convert("RGB")

        params = {
            **m_settings.THUMBNAIL_SAVE_PARAMS_BY_FORMAT,
            **kwargs,
            "format": self.out_format,
        }

        tmp_image = BytesIO()
        image.save(tmp_image, **params)
        self.storage.save(self.name, tmp_image)
        self._saved = True

        # if m_settings.THUMBNAIL_IMAGE_OPTIMIZE_HANDLER:
        #     optimze_handler = import_string(m_settings.THUMBNAIL_IMAGE_OPTIMIZE_HANDLER)
        #     optimze_handler(self)

    save.alters_data = True


DefaultThumbnailImage: Final = m_settings.THUMBNAIL_IMAGE_CLASS
