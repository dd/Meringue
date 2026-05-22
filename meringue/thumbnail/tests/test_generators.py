from pathlib import Path
from unittest import mock

import pytest

from meringue.thumbnail.exceptions import WrongActionOrPropertyError
from meringue.thumbnail.exceptions import WrongFormatError
from meringue.thumbnail.generators import Thumbnailer


class TestThumbnailer:
    def test_requires_absolute_path(self):
        with pytest.raises(AttributeError):
            Thumbnailer(Path("relative/path.png"), job_chain=["resize"])

    def test_accepts_absolute_path(self, tmp_image_path):
        t = Thumbnailer(tmp_image_path, job_chain=["resize"])
        assert t.source_image_path == tmp_image_path

    def test_make_thumbnail_with_resize(self, tmp_image_path):
        t = Thumbnailer(tmp_image_path, job_chain=["s:100x50", "resize"])
        image = t.make_thumbnail()
        assert image.size == (100, 50)

    def test_make_thumbnail_with_crop(self, tmp_image_path):
        t = Thumbnailer(tmp_image_path, job_chain=["s:100x100", "resize", "crop"])
        image = t.make_thumbnail()
        assert image.size == (100, 100)

    def test_make_thumbnail_with_properties(self, tmp_image_path):
        t = Thumbnailer(
            tmp_image_path,
            job_chain=["s:50x50", "rm:cover", "resize", "crop"],
        )
        image = t.make_thumbnail()
        assert image.size == (50, 50)

    def test_wrong_action_raises(self, tmp_image_path):
        t = Thumbnailer(tmp_image_path, job_chain=["nonexistent_action"])
        with pytest.raises(WrongActionOrPropertyError):
            t.make_thumbnail()

    def test_get_thumbnail_wrong_format_raises(self, tmp_image_path):
        t = Thumbnailer(tmp_image_path, job_chain=["s:100x100", "resize"])
        with pytest.raises(WrongFormatError):
            t.get_thumbnail("AVIF")

    def test_get_thumbnail_returns_thumbnail_image(self, tmp_image_path):
        storage = mock.MagicMock()
        storage.path.return_value = Path("/tmp/nonexistent_thumb.png")
        t = Thumbnailer(tmp_image_path, job_chain=["s:50x50", "resize"], storage=storage)
        result = t.get_thumbnail("PNG")
        assert result.out_format == "PNG"
        storage.save.assert_called_once()

    def test_get_thumbnail_uses_lazy_make(self, tmp_image_path):
        storage = mock.MagicMock()
        storage.path.return_value = Path("/tmp/nonexistent.png")
        t = Thumbnailer(tmp_image_path, job_chain=["s:50x50", "resize"], storage=storage)
        result = t.get_thumbnail("PNG")
        assert result.source_image_path == tmp_image_path
