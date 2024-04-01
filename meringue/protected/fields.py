from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.files import FileField
from django.db.models.fields.files import FieldFile
from django.db.models.fields.files import ImageField
from django.db.models.fields.files import ImageFieldFile
from django.urls import reverse


class ProtectedFileMixin:
    @property
    def url(self):
        self._require_file()
        result_url = reverse(
            "meringue-protected-file",
            kwargs={
                "contenttype_id": ContentType.objects.get_for_model(self.instance.__class__).id,
                "field": self.field.name,
                "pk": self.instance.pk,
            },
        )
        return result_url

    @property
    def original_url(self):
        self._require_file()
        return self.storage.url(self.name)


class ProtectedFieldFile(ProtectedFileMixin, FieldFile):
    pass


class ProtectedFileField(FileField):
    attr_class = ProtectedFieldFile

    def __init__(self, verbose_name=None, name=None, upload_to="protected", storage=None, **kwargs):
        super().__init__(verbose_name, name, upload_to, storage, **kwargs)


class ProtectedImageFieldFile(ProtectedFileMixin, ImageFieldFile):
    pass


class ProtectedImageField(ImageField):
    attr_class = ProtectedImageFieldFile

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        kwargs.setdefault("upload_to", "protected")
        super().__init__(verbose_name, name, width_field, height_field, **kwargs)
