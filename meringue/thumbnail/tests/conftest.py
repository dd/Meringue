from pathlib import Path

import pytest

from PIL import Image


@pytest.fixture()
def rgba_image():
    return Image.new("RGBA", (200, 100), color=(255, 0, 0, 255))


@pytest.fixture()
def rgb_image():
    return Image.new("RGB", (200, 100), color=(255, 0, 0))


@pytest.fixture()
def tmp_image_path(tmp_path, rgba_image):
    path = tmp_path / "source.png"
    rgba_image.save(path, format="PNG")
    return path


@pytest.fixture()
def tmp_jpeg_path(tmp_path, rgb_image):
    path = tmp_path / "source.jpg"
    rgb_image.save(path, format="JPEG")
    return path
