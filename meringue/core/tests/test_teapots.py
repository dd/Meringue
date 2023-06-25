from django.test import Client
from django.urls import reverse

import pytest


@pytest.mark.django_db
def test_cmtimemixin():
    """
    Nominal mixin check
    """
    client = Client()
    response = client.get(reverse("make_coffee"))
    assert response.status_code == 418
