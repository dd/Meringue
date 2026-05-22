from pathlib import Path
from unittest import mock

import pytest

from PIL import Image

from meringue.thumbnail.constants import FORMAT_JPEG
from meringue.thumbnail.constants import FORMAT_PNG
from meringue.thumbnail.constants import FORMAT_WEBP
from meringue.thumbnail.images import ThumbnailImage


@pytest.fixture()
def thumb(rgba_image, tmp_path):
    storage = mock.MagicMock()
    storage.path.return_value = tmp_path / "ab" / "cd" / "abcd.png"
    storage.url.return_value = "/media/m/thumbnail/ab/cd/abcd.png"

    return ThumbnailImage(
        image_path=Path("/source/image.png"),
        job_chain=["s:100x100", "resize"],
        out_format=FORMAT_PNG,
        image=rgba_image,
        storage=storage,
    )


class TestThumbnailImage:
    def test_name_is_split_into_directories(self, thumb):
        name = thumb.name
        assert len(name.parts) == 3
        filename = name.parts[-1]
        assert name.parts[0] == filename[:2]
        assert name.parts[1] == filename[2:4]

    def test_thumbnail_hash_is_md5(self, thumb):
        h = thumb.thumbnail_hash
        assert len(h) == 32
        assert all(c in "0123456789abcdef" for c in h)

    def test_thumbnail_hash_is_cached(self, thumb):
        h1 = thumb.thumbnail_hash
        h2 = thumb.thumbnail_hash
        assert h1 is h2

    def test_file_extension_for_png(self, thumb):
        assert thumb.file_extension == ".png"

    def test_file_extension_for_jpeg(self, rgba_image):
        thumb = ThumbnailImage(
            image_path=Path("/source/image.jpg"),
            job_chain=["resize"],
            out_format=FORMAT_JPEG,
            image=rgba_image,
        )
        assert thumb.file_extension == ".jpg"

    def test_filename_contains_hash_and_extension(self, thumb):
        assert thumb.filename == f"{thumb.thumbnail_hash}{thumb.file_extension}"

    def test_is_supports_alpha_png(self, thumb):
        assert thumb.is_supports_alpha is True

    def test_is_supports_alpha_jpeg(self, rgba_image):
        thumb = ThumbnailImage(
            image_path=Path("/source/image.jpg"),
            job_chain=[],
            out_format=FORMAT_JPEG,
            image=rgba_image,
        )
        assert thumb.is_supports_alpha is False

    def test_mimetype_png(self, thumb):
        assert thumb.mimetype == "image/png"

    def test_mimetype_webp(self, rgba_image):
        thumb = ThumbnailImage(
            image_path=Path("/source/image.webp"),
            job_chain=[],
            out_format=FORMAT_WEBP,
            image=rgba_image,
        )
        assert thumb.mimetype == "image/webp"

    def test_mimetype_jpeg(self, rgba_image):
        thumb = ThumbnailImage(
            image_path=Path("/source/image.jpg"),
            job_chain=[],
            out_format=FORMAT_JPEG,
            image=rgba_image,
        )
        assert thumb.mimetype == "image/jpeg"

    def test_saved_false_when_not_on_disk(self, thumb):
        assert thumb.saved is False

    def test_saved_true_when_on_disk(self, thumb, tmp_path):
        path = thumb.storage.path.return_value
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        thumb._saved = None
        assert thumb.saved is True

    def test_save_writes_to_storage(self, thumb):
        thumb._saved = False
        thumb.save()
        thumb.storage.save.assert_called_once()

    def test_save_skips_if_already_saved(self, thumb):
        thumb._saved = True
        thumb.save()
        thumb.storage.save.assert_not_called()

    def test_save_force_overwrites(self, thumb):
        thumb._saved = True
        thumb.save(force=True)
        thumb.storage.save.assert_called_once()

    def test_save_converts_to_rgb_for_jpeg(self, rgba_image):
        storage = mock.MagicMock()
        storage.path.return_value = Path("/tmp/test.jpg")
        thumb = ThumbnailImage(
            image_path=Path("/source/image.jpg"),
            job_chain=[],
            out_format=FORMAT_JPEG,
            image=rgba_image,
            storage=storage,
        )
        thumb._saved = False
        thumb.save()
        storage.save.assert_called_once()

    def test_different_sources_produce_different_hashes(self, rgba_image):
        t1 = ThumbnailImage(
            image_path=Path("/source/a.png"),
            job_chain=["resize"],
            out_format=FORMAT_PNG,
            image=rgba_image,
        )
        t2 = ThumbnailImage(
            image_path=Path("/source/b.png"),
            job_chain=["resize"],
            out_format=FORMAT_PNG,
            image=rgba_image,
        )
        assert t1.thumbnail_hash != t2.thumbnail_hash

    def test_different_jobs_produce_different_hashes(self, rgba_image):
        t1 = ThumbnailImage(
            image_path=Path("/source/a.png"),
            job_chain=["s:100x100", "resize"],
            out_format=FORMAT_PNG,
            image=rgba_image,
        )
        t2 = ThumbnailImage(
            image_path=Path("/source/a.png"),
            job_chain=["s:200x200", "resize"],
            out_format=FORMAT_PNG,
            image=rgba_image,
        )
        assert t1.thumbnail_hash != t2.thumbnail_hash
