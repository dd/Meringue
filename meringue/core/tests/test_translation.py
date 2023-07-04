from test_project.models import TranslatedModel


def test_translate_fields():
    """
    Checking the registration of fields for translation
    """

    instance = TranslatedModel()
    assert hasattr(instance, "name")
    assert hasattr(instance, "name_ru")
    assert hasattr(instance, "name_en")
