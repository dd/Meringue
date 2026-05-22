from pathlib import Path
from unittest import mock

import pytest

from django.test import override_settings

from meringue.thumbnail.shortcuts import _dummyimage
from meringue.thumbnail.shortcuts import get_thumbnail


class TestDummyImage:
    @override_settings(DEBUG=True)
    def test_debug_extracts_size_from_job_chain(self):
        url = _dummyimage(["s:100x200", "resize"])
        assert "100" in url
        assert "200" in url

    @override_settings(DEBUG=True)
    def test_debug_defaults_to_42x42(self):
        url = _dummyimage(["resize"])
        assert "42" in url

    @override_settings(DEBUG=False, STATIC_URL="/static/")
    def test_production_returns_static(self):
        url = _dummyimage(["s:100x200"])
        assert url == "/static/images/noise.png"


class TestGetThumbnail:
    def test_returns_dummy_for_missing_file(self):
        path = Path("/nonexistent/image.png")
        result = get_thumbnail(path, ["s:100x100", "resize"])
        assert isinstance(result, str)

    def test_returns_url_for_existing_file(self, tmp_image_path):
        storage = mock.MagicMock()
        storage.path.return_value = Path("/tmp/nonexistent.png")
        storage.url.return_value = "/media/thumbnail/test.png"

        with mock.patch(
            "meringue.thumbnail.shortcuts.DefaultThumbnailer"
        ) as MockThumbnailer:
            mock_thumbnail = mock.MagicMock()
            mock_thumbnail.url = "/media/thumbnail/test.png"
            MockThumbnailer.return_value.get_thumbnail.return_value = mock_thumbnail

            result = get_thumbnail(tmp_image_path, ["s:100x100", "resize"])
            assert result == "/media/thumbnail/test.png"
            MockThumbnailer.assert_called_once_with(tmp_image_path, job_chain=["s:100x100", "resize"])
