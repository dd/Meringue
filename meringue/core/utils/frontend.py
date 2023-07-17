from urllib.parse import urljoin

from meringue.conf import m_settings


__all__ = [
    "get_link",
]


def get_link(
    url_name: str,
    absolute: bool | None = True,
    **kwargs,
) -> str:
    """
    Method for getting a link.

    Attributes:
        url_name: The url name
        absolute: Flag to make URL absolute or relative
        kwargs: Url parameters

    Raises:
        Exception: FRONTEND_URLS parameter is empty
        Exception: The passed link is not specified in the FRONTEND_URLS parameter
        Exception: FRONTEND_DOMAIN parameter not specified

    Returns:
        link to the front.
    """

    if m_settings.FRONTEND_URLS is None:
        msg = "FRONTEND_URLS parameter is empty"
        raise Exception(msg)

    if url_name not in m_settings.FRONTEND_URLS:
        msg = f"The passed link `{url_name}` is not specified in the FRONTEND_URLS parameter"
        raise Exception(msg)

    url = m_settings.FRONTEND_URLS[url_name]
    url = url(**kwargs) if callable(url) else url.format(**kwargs)

    if absolute:
        if m_settings.FRONTEND_DOMAIN is None:
            msg = "FRONTEND_DOMAIN option not set"
            raise Exception(msg)

        url = urljoin(m_settings.FRONTEND_DOMAIN, url)

    return url
