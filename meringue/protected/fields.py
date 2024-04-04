from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.files import FileField
from django.db.models.fields.files import FieldFile
from django.db.models.fields.files import ImageField
from django.db.models.fields.files import ImageFieldFile
from django.urls import reverse
try:
    from django_hosts.resolvers import reverse as hosts_reverse
except ImportError:
    hosts_reverse = None

from meringue.conf import m_settings


class ProtectedFileMixin:
    @property
    def url(self):
        """
        Link to the view with access verification to the file
        """

        self._require_file()

        reverse_kwargs = {
            "cid": ContentType.objects.get_for_model(self.instance.__class__).id,
            "field": self.field.name,
            "pk": self.instance.pk,
            "disp": self.field.m_protected_disposition,
        }
        if self.field.m_protected_host_name:
            result_url = hosts_reverse(
                self.field.m_protected_view_name,
                kwargs=reverse_kwargs,
                host=self.field.m_protected_host_name,
            )
        else:
            result_url = reverse(self.field.m_protected_view_name, kwargs=reverse_kwargs)
        return result_url

    @property
    def redirect_url(self):
        """
        Link to the file where nginx should serve it after access verification.
        """

        return self.field.m_protected_nginx_location_getter(self)

    @property
    def original_url(self):
        """
        The original link to the file.
        """

        self._require_file()
        return self.storage.url(self.name)


class ProtectedFieldFile(ProtectedFileMixin, FieldFile):
    pass


class ProtectedFileField(FileField):
    """
    A field that adds the mechanism of a protected file.
    """

    attr_class = ProtectedFieldFile

    def __init__(
        self,
        view_name,
        verbose_name=None,
        name=None,
        upload_to="protected",
        storage=None,
        host_name=None,
        disposition="attachment",
        nginx_location_getter=m_settings.PROTECTED_NGINX_LOCATION_GETTER,
        **kwargs,
    ):
        self.m_protected_view_name = view_name
        self.m_protected_host_name = host_name
        self.m_protected_disposition = disposition
        self.m_protected_nginx_location_getter = nginx_location_getter
        super().__init__(verbose_name, name, upload_to, storage, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['view_name'] = self.m_protected_view_name
        return name, path, args, kwargs


class ProtectedImageFieldFile(ProtectedFileMixin, ImageFieldFile):
    pass


class ProtectedImageField(ImageField):
    """
    A field that adds the mechanism of a protected image.
    """

    attr_class = ProtectedImageFieldFile

    def __init__(
        self,
        view_name,
        verbose_name=None,
        name=None,
        width_field=None,
        height_field=None,
        host_name=None,
        disposition="attachment",
        nginx_location_getter=m_settings.PROTECTED_NGINX_LOCATION_GETTER,
        **kwargs,
    ):
        kwargs.setdefault("upload_to", "protected")
        self.m_protected_view_name = view_name
        self.m_protected_host_name = host_name
        self.m_protected_disposition = disposition
        self.m_protected_nginx_location_getter = nginx_location_getter
        super().__init__(verbose_name, name, width_field, height_field, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['view_name'] = self.m_protected_view_name
        return name, path, args, kwargs
