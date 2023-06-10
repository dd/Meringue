from typing import Final


__all__ = [
    "UPLOAD_RENAME_HANDLER",
]


# CORE ############################################################################################

UPLOAD_RENAME_HANDLER: Final[str] = 'meringue.core.upload_handlers.rename_handler'
"""
Path to method for renaming images on upload
"""
