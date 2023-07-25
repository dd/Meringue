import json

from django.core.serializers.json import DjangoJSONEncoder


__all__ = [
    "OpenAPISchemaPatcher",
]


class OpenAPISchemaPatcher:
    """
    OpenApi3 patcher.

    https://swagger.io/specification/

    !!! info
        `json.loads` -> `json.dumps` - for render locale `__proxy__` (e.g. `gettext_lazy`)
    """

    def __init__(self):
        self._security_schemes = {}
        self._components_schemes = {}
        self._tags_schemes = {}

    def register_security_scheme(self, name: str, scheme: dict):
        """
        Register security scheme.

        Attributes:
            name: Security scheme name.
            scheme: Security scheme in [Security Scheme Object](https://swagger.io/specification/#s
                ecurity-scheme-object) or [Reference Object format](https://swagger.io/specificatio
                n/#reference-object).

        Raises:
            Exception: Security scheme already registered.
        """

        if name in self._security_schemes:
            msg = f"Security scheme named `{name}` is already registered"
            raise Exception(msg)

        self._security_schemes[name] = scheme

    def register_component_scheme(self, name: str, scheme: dict):
        """
        Register components scheme.

        Attributes:
            name: Component name.
            schema: [Formatted](https://swagger.io/specification/#schema-object) Component schema
                object.

        Raises:
            Exception: Scheme is already registered.
        """

        if name in self._components_schemes:
            msg = f"Component named `{name}` is already registered"
            raise Exception(msg)

        self._components_schemes[name] = scheme

    def register_tag(self, scheme: dict):
        """
        Register tag.

        Attributes:
            scheme: [Tag scheme object](https://swagger.io/specification/#tag-object).

        Raises:
            Exception: Tag is already registered.
        """
        name = scheme["name"]

        if name in self._tags_schemes:
            msg = f"A tag named `{name}` is already registered"
            raise Exception(msg)

        self._tags_schemes[name] = scheme

    def patch_description(self, openapi_schema: dict):
        """
        Adds a list of servers from the openapi schema source servers to the description.

        This method adds to the end of the description a list of servers that it takes from the
        [corresponding section](https://swagger.io/specification/#server-object) of the openapi
        schema.

        Attributes:
            openapi_schema: OpenAPI Object.
        """

        if not openapi_schema.get("servers", []):
            return

        openapi_schema.setdefault("info", {})
        openapi_schema["info"].setdefault("description", "")

        for server in openapi_schema["servers"]:
            name = server["description"]
            full_url = server["url"]
            clear_url = full_url.split("://")[1] if "://" in full_url else full_url
            if openapi_schema["info"]["description"]:
                openapi_schema["info"]["description"] += "\n\n"
            openapi_schema["info"]["description"] += f"{name} API: [{clear_url}]({full_url})"

    def patch_security_schemes(self, openapi_schema: dict):
        """
        Adds registered security schemes to the openapi schema.

        Attributes:
            openapi_schema: OpenAPI Object.

        Raises:
            Exception: Security scheme already registered.
        """

        if not self._security_schemes:
            return

        openapi_schema.setdefault("components", {})
        openapi_schema["components"].setdefault("securitySchemes", {})

        tmp_schemes = json.loads(json.dumps(self._security_schemes, cls=DjangoJSONEncoder))

        for name, schema in tmp_schemes.items():
            if name in openapi_schema["components"]["securitySchemes"]:
                msg = f"Security scheme named `{name}` exists in the original schema"
                raise Exception(msg)

            openapi_schema["components"]["securitySchemes"][name] = schema

    def patch_component_schemes(self, openapi_schema: dict):
        """
        Adds registered components schemas to the openapi schema.

        Attributes:
            openapi_schema: OpenAPI Object.

        Raises:
            Exception: Component schema is already registered.
        """

        if not self._components_schemes:
            return

        openapi_schema.setdefault("components", {})
        openapi_schema["components"].setdefault("schemas", {})

        tmp_components = json.loads(json.dumps(self._components_schemes, cls=DjangoJSONEncoder))

        for name, schema in tmp_components.items():
            if name in openapi_schema["components"]["schemas"]:
                msg = f"Component named `{name}` exists in the original schema"
                raise Exception(msg)

            openapi_schema["components"]["schemas"][name] = schema

    def patch_tags(self, openapi_schema: dict):
        """
        Adds registered components schemas to the openapi schema.

        Attributes:
            openapi_schema: OpenAPI Object.

        Raises:
            Exception: A tag exists in the original schema.
        """

        if not self._tags_schemes:
            return

        openapi_schema.setdefault("tags", [])
        exists_tags_schemes = (t["name"] for t in openapi_schema["tags"])
        tmp_tags = json.loads(json.dumps(self._tags_schemes, cls=DjangoJSONEncoder))

        for name, schema in tmp_tags.items():
            if name in exists_tags_schemes:
                msg = f"A tag named `{name}` exists in the original schema"
                raise Exception(msg)

            openapi_schema["tags"].append(schema)

    def patch_schema(self, openapi_schema: dict):
        """
        Fully patch the schema.
        """
        self.patch_description(openapi_schema)
        self.patch_security_schemes(openapi_schema)
        self.patch_component_schemes(openapi_schema)
        self.patch_tags(openapi_schema)
