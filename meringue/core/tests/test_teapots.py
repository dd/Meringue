from django.test import Client
from django.urls import reverse


def test_check_teapot():
    """
    Im a teapot
    """
    client = Client()
    response = client.get(reverse("make_coffee"))
    assert response.status_code == 418
