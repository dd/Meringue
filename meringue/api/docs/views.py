from drf_spectacular.views import SpectacularAPIView
from rest_framework.response import Response


__all__ = [
    "MeringueSpectacularAPIView",
]


class MeringueSpectacularAPIView(SpectacularAPIView):
    """
    Spectacular wrapper that patches the schema.
    """

    patcher = None

    def patch_schema(self, openapi_schema: dict):
        """
        Method patching OpenAPI3 object.

        Attributes:
            openapi_schema: OpenAPI Object.
        """

        if self.patcher:
            self.patcher.patch_schema(openapi_schema)

    def _get_schema_response(self, request):
        """
        Copy of [SpectacularAPIView._get_schema_response][drf_spectacular.views.SpectacularAPIView.
        _get_schema_response] but with schema patch
        """
        version = self.api_version or request.version or self._get_version_parameter(request)
        generator = self.generator_class(
            urlconf=self.urlconf, api_version=version, patterns=self.patterns
        )
        final_schema = generator.get_schema(request=request, public=self.serve_public)
        self.patch_schema(final_schema)
        return Response(
            data=final_schema,
            headers={
                "Content-Disposition": f'inline; filename="{self._get_filename(request, version)}"',
            },
        )
