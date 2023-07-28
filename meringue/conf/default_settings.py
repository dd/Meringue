from typing import Final

from django.conf import settings


# CORE #############################################################################################

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

Specify 1 to display the period for the second year.
"""

CRYPTO_KEY: Final[str] = settings.SECRET_KEY[:32]
"""
Encryption key
"""

FRONTEND_URLS: Final[dict] = None
"""
A dict of links to the frontend
"""

FRONTEND_DOMAIN: Final[str] = None
"""
Domain for generating absolute links
"""


# API ##############################################################################################

API_ENABLE_ROOT_VIEW: Final[str] = settings.DEBUG
"""
Option to enable or disable the root view of the [Router][meringue.api.routers.MeringueRouter]
"""
