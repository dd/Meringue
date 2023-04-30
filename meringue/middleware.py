import re

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404


hosts_middleware = "django_hosts.middleware.HostsMiddleware"
site_middleware = "meringue.middleware.SiteMiddleware"


class SiteMiddleware:
    """
    Подставляет SITE_ID и SITE_NAME при запросе, используется при связке с django-hosts
    """

    def process_request(self, request):
        middlewares = list(settings.MIDDLEWARE_CLASSES)
        if middlewares.index(hosts_middleware) > middlewares.index(site_middleware):
            msg = (
                "The django_hosts and simple middlewares are in the wrong order. Make sure "
                f"{hosts_middleware} comes before {site_middleware} in the MIDDLEWARE_CLASSES "
                "setting."
            )
            raise ImproperlyConfigured(msg)

        r = r"^(.[^:]+)"
        host = re.findall(r, request.get_host())[0]
        site = get_object_or_404(Site, domain=host)
        settings.SITE_ID = site.id
        settings.SITE_NAME = site.name
        # Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko
