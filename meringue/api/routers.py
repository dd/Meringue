from collections import OrderedDict
from collections import namedtuple

from rest_framework.routers import DefaultRouter

from meringue.conf import m_settings


ObjectRoute = namedtuple("ObjectRoute", ["url", "mapping", "name", "detail", "initkwargs"])
"""
Object predefined detail route.
"""


class MeringueRouter(DefaultRouter):
    """
    The default router is inherited from the original default router but with some modifications.
    """

    root_view_name = "index"
    routes = [  # noqa: RUF012
        # Object predefined detail route.
        ObjectRoute(
            url=r"^{prefix}{trailing_slash}$",
            mapping={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            name="{basename}",
            detail=True,
            initkwargs={},
        ),
        *DefaultRouter.routes,
    ]

    @property
    def include_root_view(self):
        return m_settings.API_ENABLE_ROOT_VIEW

    def get_api_root_view(self, api_urls=None):
        """
        Return a basic root view.
        """

        api_root_dict = OrderedDict()
        object_name = self.routes[0].name
        list_name = self.routes[1].name
        for prefix, viewset, basename in self.registry:
            if getattr(viewset, "m_object_detail", False):
                api_root_dict[prefix] = object_name.format(basename=basename)
            else:
                api_root_dict[prefix] = list_name.format(basename=basename)

        return self.APIRootView.as_view(api_root_dict=api_root_dict)

    def get_routes(self, viewset):
        """
        Extra routes are filtered according to the new route type.
        """

        tmp_routes = super().get_routes(viewset)
        is_object_viewset = getattr(viewset, "m_object_detail", False)

        routes = []
        for route in tmp_routes:
            is_object_route = isinstance(route, ObjectRoute)

            if is_object_viewset:
                is_list_view = route.name == "{basename}-list"
                is_detail_view = route.name == "{basename}-detail"

                if is_list_view or is_detail_view:
                    # ignore default list and detail routes
                    continue

                routes.append(route)

            elif not is_object_route:
                routes.append(route)

        return routes
