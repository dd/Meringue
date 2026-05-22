from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from meringue.thumbnail.drf_fields import BaseImageField
from meringue.thumbnail.drf_fields import get_format_from_path
from meringue.thumbnail.drf_fields import MImageField
from meringue.thumbnail.drf_fields import MImageSetField


class TestGetFormatFromPath:
    @pytest.mark.parametrize(
        "suffix, expected",
        [
            (".png", "PNG"),
            (".jpg", "JPEG"),
            (".jpeg", "JPEG"),
            (".webp", "WEBP"),
            (".gif", "GIF"),
        ],
    )
    def test_known_extensions(self, suffix, expected):
        path = Path(f"/image{suffix}")
        assert get_format_from_path(path) == expected

    def test_unknown_extension_raises(self):
        with pytest.raises(KeyError):
            get_format_from_path(Path("/image.avif"))


class TestBaseImageField:
    def test_size_creates_job_chain(self):
        field = BaseImageField(size=(100, 100))
        assert "s:100x100" in field.job_chain
        assert "resize" in field.job_chain

    def test_job_chain_passthrough(self):
        chain = ["s:200x200", "rm:cover", "resize"]
        field = BaseImageField(job_chain=chain)
        assert field.job_chain == chain

    def test_no_args_empty_chain(self):
        field = BaseImageField()
        assert field.job_chain == []

    def test_both_size_and_job_chain_raises(self):
        with pytest.raises(ValueError):
            BaseImageField(size=(100, 100), job_chain=["resize"])


class TestMImageSetField:
    def test_size_creates_job_chains_with_dimensions(self):
        field = MImageSetField(size=(100, 100), dimensions=(1, 2))
        assert 1 in field.job_chains
        assert 2 in field.job_chains
        assert "s:100x100" in field.job_chains[1]
        assert "s:200x200" in field.job_chains[2]

    def test_dimension_1_added_if_missing(self):
        field = MImageSetField(size=(100, 100), dimensions=(2,))
        assert 1 in field.job_chains

    def test_both_size_and_job_chains_raises(self):
        with pytest.raises(ValueError):
            MImageSetField(size=(100, 100), job_chains={1: ["resize"]})

    def test_no_args_empty_chains(self):
        field = MImageSetField()
        assert field.job_chains == {}

    def test_size_without_dimensions_raises(self):
        with pytest.raises(ValueError):
            MImageSetField(size=(100, 100), dimensions=None)

    def test_custom_base_job_chain(self):
        field = MImageSetField(size=(100, 100), base_job_chain=["rm:contain", "resize"])
        assert "rm:contain" in field.job_chains[1]
        assert "resize" in field.job_chains[1]

    def test_job_chains_passthrough(self):
        chains = {1: ["s:100x100", "resize"], 2: ["s:200x200", "resize"]}
        field = MImageSetField(job_chains=chains)
        assert field.job_chains is chains


class TestMImageFieldRepresentation:
    def test_falsy_value_returns_none(self):
        field = MImageField()
        assert field.to_representation(None) is None
        assert field.to_representation("") is None

    @patch("meringue.thumbnail.drf_fields.DefaultThumbnailer")
    def test_existing_file(self, mock_thumbnailer_cls, tmp_path):
        image_path = tmp_path / "photo.png"
        image_path.write_bytes(b"fake")

        mock_thumbnail = MagicMock()
        mock_thumbnail.url = "/media/thumb.png"
        mock_thumbnailer_cls.return_value.get_thumbnail.return_value = mock_thumbnail

        value = MagicMock()
        value.path = str(image_path)
        value.__bool__ = lambda self: True

        field = MImageField(size=(100, 100))
        result = field.to_representation(value)

        assert result == "/media/thumb.png"
        mock_thumbnailer_cls.assert_called_once_with(image_path, job_chain=field.job_chain)
        mock_thumbnailer_cls.return_value.get_thumbnail.assert_called_once_with("PNG")

    @patch("meringue.thumbnail.drf_fields._dummyimage")
    def test_missing_file(self, mock_dummyimage):
        mock_dummyimage.return_value = "//dummyimage.com/42x42"

        value = MagicMock()
        value.path = "/nonexistent/photo.png"
        value.__bool__ = lambda self: True

        field = MImageField(size=(100, 100))
        result = field.to_representation(value)

        assert result == "//dummyimage.com/42x42"
        mock_dummyimage.assert_called_once_with([])


class TestMImageSetFieldRepresentation:
    def test_falsy_value_returns_none(self):
        field = MImageSetField(size=(100, 100))
        assert field.to_representation(None) is None
        assert field.to_representation("") is None

    @patch("meringue.thumbnail.drf_fields._dummyimage")
    def test_missing_file(self, mock_dummyimage):
        mock_dummyimage.return_value = "//dummyimage.com/100x100"

        value = MagicMock()
        value.path = "/nonexistent/photo.png"
        value.__bool__ = lambda self: True

        field = MImageSetField(size=(100, 100))
        result = field.to_representation(value)

        assert len(result) == 1
        assert result[0]["url"] == "//dummyimage.com/100x100"
        assert result[0]["type"] == "image/png"

    @patch("meringue.thumbnail.drf_fields.DefaultThumbnailer")
    def test_existing_file(self, mock_thumbnailer_cls, tmp_path):
        image_path = tmp_path / "photo.png"
        image_path.write_bytes(b"fake")

        mock_original = MagicMock()
        mock_original.url = "/media/original.png"
        mock_original.mimetype = "image/png"

        mock_webp = MagicMock()
        mock_webp.url = "/media/thumb.webp"
        mock_webp.mimetype = "image/webp"

        mock_thumbnailer_cls.return_value.get_thumbnail.side_effect = [
            mock_original,
            mock_webp,
            mock_original,
            mock_webp,
        ]

        value = MagicMock()
        value.path = str(image_path)
        value.__bool__ = lambda self: True

        field = MImageSetField(size=(100, 100), dimensions=(1, 2))
        result = field.to_representation(value)

        assert len(result) == 2
        assert "1x" in result[0]["srcset"]
        assert "2x" in result[0]["srcset"]
        assert result[0]["type"] == "image/webp"
        assert result[1]["type"] == "image/png"
