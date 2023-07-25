from unittest.mock import patch

import pytest

from meringue.api.docs.patchers import OpenAPISchemaPatcher
from meringue.api.docs.tests.conftest import schema_1
from meringue.api.docs.tests.conftest import schema_1_result
from meringue.api.docs.tests.conftest import schema_2
from meringue.api.docs.tests.conftest import schema_2_result


def test_patch_description():
    """
    Checking the completion of the description of the list of servers
    """

    patcher = OpenAPISchemaPatcher()
    patcher.patch_description(schema_1)
    assert schema_1 == schema_1_result


def test_patch_description_with_empty_servers():
    """
    Checking the filling of the description with an empty list of servers
    """

    patcher = OpenAPISchemaPatcher()
    schema = {"servers": []}
    patcher.patch_description(schema)
    assert schema == {"servers": []}


def test_patch_description_with_filled_description():
    """
    Checking the completion of the description with a pre-filled description
    """

    patcher = OpenAPISchemaPatcher()
    patcher.patch_description(schema_2)
    assert schema_2 == schema_2_result


def test_patch_security():
    """
    Patch security components
    """

    patcher = OpenAPISchemaPatcher()
    patcher.register_security_scheme("Test Security", {})
    schema = {}
    patcher.patch_security_schemes(schema)
    assert schema == {"components": {"securitySchemes": {"Test Security": {}}}}


def test_patch_security_without_register():
    """
    Populating components without registered
    """

    patcher = OpenAPISchemaPatcher()
    schema = {}
    patcher.patch_security_schemes(schema)
    assert schema == {}


def test_register_security_twice():
    """
    Trying to register two security with the same name
    """

    patcher = OpenAPISchemaPatcher()
    patcher.register_security_scheme("Test Security", {})
    msg = "Security scheme named `Test Security` is already registered"
    with pytest.raises(Exception, match=msg):
        patcher.register_security_scheme("Test Security", {})


def test_register_exist_security():
    """
    Attempt to register a component already in the schema
    """

    patcher = OpenAPISchemaPatcher()
    patcher.register_security_scheme("Test Security", {})
    msg = "Security scheme named `Test Security` exists in the original schema"
    with pytest.raises(Exception, match=msg):
        patcher.patch_security_schemes({"components": {"securitySchemes": {"Test Security": {}}}})


def test_patch_components():
    """
    Patch components
    """

    patcher = OpenAPISchemaPatcher()
    patcher.register_component_scheme("Test component", {})
    schema = {}
    patcher.patch_component_schemes(schema)
    assert schema == {"components": {"schemas": {"Test component": {}}}}


def test_patch_components_without_register():
    """
    Populating components without registered
    """

    patcher = OpenAPISchemaPatcher()
    schema = {}
    patcher.patch_component_schemes(schema)
    assert schema == {}


def test_register_component_twice():
    """
    Trying to register two components with the same name
    """

    patcher = OpenAPISchemaPatcher()
    patcher.register_component_scheme("Test component", {})
    with pytest.raises(Exception, match="Component named `Test component` is already registered"):
        patcher.register_component_scheme("Test component", {})


def test_register_exist_component():
    """
    Attempt to register a component already in the schema
    """

    patcher = OpenAPISchemaPatcher()
    patcher.register_component_scheme("Test component", {})
    msg = "Component named `Test component` exists in the original schema"
    with pytest.raises(Exception, match=msg):
        patcher.patch_component_schemes({"components": {"schemas": {"Test component": {}}}})


def test_patch_tags():
    """
    Patch tags
    """

    patcher = OpenAPISchemaPatcher()
    patcher.register_tag({"name": "Test tag"})
    schema = {}
    patcher.patch_tags(schema)
    assert schema == {"tags": [{"name": "Test tag"}]}


def test_patch_tags_without_register():
    """
    Populating tags without registered
    """

    patcher = OpenAPISchemaPatcher()
    schema = {}
    patcher.patch_tags(schema)
    assert schema == {}


def test_register_tag_twice():
    """
    Trying to register two tags with the same name
    """

    patcher = OpenAPISchemaPatcher()
    patcher.register_tag({"name": "Test tag"})
    with pytest.raises(Exception, match="A tag named `Test tag` is already registered"):
        patcher.register_tag({"name": "Test tag"})


def test_register_exist_tag():
    """
    Attempt to register a tag already in the schema
    """

    patcher = OpenAPISchemaPatcher()
    patcher.register_tag({"name": "Test tag"})
    with pytest.raises(Exception, match="A tag named `Test tag` exists in the original schema"):
        patcher.patch_tags({"tags": [{"name": "Test tag"}]})


@patch.object(OpenAPISchemaPatcher, "patch_tags")
@patch.object(OpenAPISchemaPatcher, "patch_component_schemes")
@patch.object(OpenAPISchemaPatcher, "patch_security_schemes")
@patch.object(OpenAPISchemaPatcher, "patch_description")
def test_patch_fully(
    mocked_patch_description,
    mocked_patch_security_schemes,
    mocked_patch_component_schemes,
    mocked_patch_tags,
):
    patcher = OpenAPISchemaPatcher()
    schema = {}
    patcher.patch_schema(schema)
    mocked_patch_description.assert_called_once_with(schema)
    mocked_patch_security_schemes.assert_called_once_with(schema)
    mocked_patch_component_schemes.assert_called_once_with(schema)
    mocked_patch_tags.assert_called_once_with(schema)
