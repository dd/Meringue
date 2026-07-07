from io import BytesIO
from pathlib import Path
from unittest import mock

from django.test import override_settings

from PIL import Image

from meringue.thumbnail.constants import FORMAT_JPEG
from meringue.thumbnail.constants import FORMAT_PNG
from meringue.thumbnail.images import ThumbnailImage
from meringue.thumbnail.optimizers import optimize
from meringue.thumbnail.optimizers import oxipng


def get_thumbnail_image(out_format=FORMAT_PNG):
    return ThumbnailImage(
        image_path=Path("/source/image.png"),
        job_chain=[],
        out_format=out_format,
        image=Image.new("RGBA", (10, 10), color=(255, 0, 0, 255)),
        storage=mock.MagicMock(),
    )


@override_settings(
    MERINGUE={
        "THUMBNAIL_OPTIMIZERS": {
            "oxipng": {"binary": "/usr/bin/oxipng", "options": ["-o", "2"]},
        },
    }
)
@mock.patch("meringue.thumbnail.optimizers.subprocess.run")
def test_oxipng_optimizes_png_from_memory(run):
    run.return_value = mock.Mock(returncode=0, stdout=b"optimized", stderr=b"")

    result = oxipng(
        get_thumbnail_image(),
        BytesIO(b"source"),
        {"binary": "/usr/bin/oxipng", "options": ["-o", "2"]},
    )

    assert result.read() == b"optimized"
    run.assert_called_once_with(
        ["/usr/bin/oxipng", "-o", "2", "--stdout", "-"],
        input=b"source",
        capture_output=True,
        check=False,
    )


@mock.patch("meringue.thumbnail.optimizers.subprocess.run")
def test_oxipng_uses_default_options(run):
    run.return_value = mock.Mock(returncode=0, stdout=b"optimized", stderr=b"")

    oxipng(get_thumbnail_image(), BytesIO(b"source"), {"binary": "/usr/bin/oxipng"})

    run.assert_called_once_with(
        [
            "/usr/bin/oxipng",
            "-o",
            "max",
            "--strip",
            "all",
            "--alpha",
            "--stdout",
            "-",
        ],
        input=b"source",
        capture_output=True,
        check=False,
    )


@mock.patch("meringue.thumbnail.optimizers.subprocess.run")
def test_oxipng_skips_non_png(run):
    image_file = BytesIO(b"source")

    result = oxipng(get_thumbnail_image(FORMAT_JPEG), image_file, {"binary": "/usr/bin/oxipng"})

    assert result is image_file
    run.assert_not_called()


@mock.patch("meringue.thumbnail.optimizers.subprocess.run")
def test_oxipng_skips_when_binary_is_not_configured(run):
    image_file = BytesIO(b"source")

    result = oxipng(get_thumbnail_image(), image_file, {"binary": None})

    assert result is image_file
    run.assert_not_called()


@mock.patch("meringue.thumbnail.optimizers.subprocess.run")
def test_oxipng_returns_original_file_on_failure(run, caplog):
    run.return_value = mock.Mock(returncode=1, stdout=b"", stderr=b"broken png")
    image_file = BytesIO(b"source")

    result = oxipng(get_thumbnail_image(), image_file, {"binary": "/usr/bin/oxipng"})

    assert result is image_file
    assert "Oxipng failed" in caplog.text


@mock.patch("meringue.thumbnail.optimizers.subprocess.run")
def test_optimize_is_noop_by_default(run):
    image_file = BytesIO(b"source")

    result = optimize(get_thumbnail_image(), image_file)

    assert result is image_file
    run.assert_not_called()


@override_settings(
    MERINGUE={
        "THUMBNAIL_OPTIMIZERS": {
            "oxipng": {"binary": "/usr/bin/oxipng", "options": ["-o", "2"]},
        },
    }
)
@mock.patch("meringue.thumbnail.optimizers.subprocess.run")
def test_optimize_runs_configured_optimizers(run):
    run.return_value = mock.Mock(returncode=0, stdout=b"optimized", stderr=b"")

    result = optimize(get_thumbnail_image(), BytesIO(b"source"))

    assert result.read() == b"optimized"


@override_settings(MERINGUE={"THUMBNAIL_OPTIMIZERS": {"unknown": {}}})
def test_optimize_skips_unknown_optimizers(caplog):
    image_file = BytesIO(b"source")

    result = optimize(get_thumbnail_image(), image_file)

    assert result is image_file
    assert "Unknown thumbnail optimizer" in caplog.text
