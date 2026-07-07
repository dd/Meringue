import logging
import subprocess
from io import BytesIO

from meringue.conf import m_settings
from meringue.thumbnail import constants


logger = logging.getLogger("meringue.thumbnail")


def optimize(thumbnail_image, image_file):
    """
    Run configured thumbnail optimizers.
    """

    optimized_image = image_file

    for optimizer_name, options in m_settings.THUMBNAIL_OPTIMIZERS.items():
        optimizer = OPTIMIZERS.get(optimizer_name)
        if optimizer is None:
            logger.warning("Unknown thumbnail optimizer `%s`.", optimizer_name)
            continue

        optimized_image.seek(0)
        optimized_image = optimizer(thumbnail_image, optimized_image, options)

    return optimized_image


def oxipng(thumbnail_image, image_file, options):
    """
    Optimize PNG thumbnail with oxipng without writing it to local disk.

    Oxipng reads the image from stdin and writes the optimized image to stdout.
    """

    if thumbnail_image.file_extension != constants.EXTENSION_PNG:
        return image_file

    binary = options.get("binary")
    if not binary:
        return image_file

    image_file.seek(0)
    result = subprocess.run(  # noqa: S603
        [
            binary,
            *options.get("options", ["-o", "max", "--strip", "all", "--alpha"]),
            "--stdout",
            "-",
        ],
        input=image_file.read(),
        capture_output=True,
        check=False,
    )

    if result.returncode != 0:
        logger.warning(
            "Oxipng failed for thumbnail `%s`: %s",
            thumbnail_image.name,
            result.stderr.decode(errors="replace").strip(),
        )
        return image_file

    return BytesIO(result.stdout)


OPTIMIZERS = {
    "oxipng": oxipng,
}
