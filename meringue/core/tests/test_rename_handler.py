from pathlib import Path
from uuid import UUID

from faker import Faker

from meringue.core.upload_handlers import rename_handler


fake = Faker()


def test_rename_handler():
    """
    Check work rename_handler
    """

    original_name = fake.file_name()
    new_name = rename_handler(original_name)

    assert Path(new_name).suffix == Path(original_name).suffix
    assert Path(new_name).stem != Path(original_name).stem


def test_rename_to_uuid4():
    """
    Checking file rename to uuid4
    """

    new_name = rename_handler(fake.file_name())
    UUID(Path(new_name).stem)
