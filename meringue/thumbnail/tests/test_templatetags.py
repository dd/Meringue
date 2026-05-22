from pathlib import Path
from unittest.mock import patch

import pytest

from meringue.thumbnail.templatetags.m_thumbnails import thumbnail


class TestThumbnailFilter:
    @patch("meringue.thumbnail.templatetags.m_thumbnails.get_thumbnail")
    def test_passes_parsed_job_chain(self, mock_get_thumbnail):
        mock_get_thumbnail.return_value = "/media/thumb.png"

        result = thumbnail("/path/to/image.png", "s:100x100,resize,crop")

        mock_get_thumbnail.assert_called_once_with(
            file_path=Path("/path/to/image.png"),
            job_chain=["s:100x100", "resize", "crop"],
        )
        assert result == "/media/thumb.png"

    @patch("meringue.thumbnail.templatetags.m_thumbnails.get_thumbnail")
    def test_empty_args(self, mock_get_thumbnail):
        mock_get_thumbnail.return_value = "/media/thumb.png"

        thumbnail("/path/to/image.png")

        mock_get_thumbnail.assert_called_once_with(
            file_path=Path("/path/to/image.png"),
            job_chain=[""],
        )

    @patch("meringue.thumbnail.templatetags.m_thumbnails.get_thumbnail")
    def test_single_action(self, mock_get_thumbnail):
        mock_get_thumbnail.return_value = "/media/thumb.png"

        thumbnail("/path/to/image.png", "resize")

        mock_get_thumbnail.assert_called_once_with(
            file_path=Path("/path/to/image.png"),
            job_chain=["resize"],
        )

    @patch("meringue.thumbnail.templatetags.m_thumbnails.get_thumbnail")
    def test_complex_chain(self, mock_get_thumbnail):
        mock_get_thumbnail.return_value = "/media/thumb.png"

        thumbnail("/path/to/image.png", "s:600x400,rm:cover,resize,s:400x400,crop")

        mock_get_thumbnail.assert_called_once_with(
            file_path=Path("/path/to/image.png"),
            job_chain=["s:600x400", "rm:cover", "resize", "s:400x400", "crop"],
        )

    @patch("meringue.thumbnail.templatetags.m_thumbnails.get_thumbnail")
    def test_returns_get_thumbnail_result(self, mock_get_thumbnail):
        mock_get_thumbnail.return_value = "//dummyimage.com/42x42"

        result = thumbnail("/nonexistent.png", "s:100x100,resize")

        assert result == "//dummyimage.com/42x42"
