from typing import Final


# CORE ############################################################################################

UPLOAD_RENAME_HANDLER: Final[str] = "meringue.core.upload_handlers.rename_handler"
"""
Path to method for renaming images on upload
"""

COP_YEAR: Final[int] = None
"""
Project start year for the copyright tag
"""

COP_YEARS_DIFF: Final[int] = 10
"""
Difference in years for which it is necessary to display the range of years
"""
