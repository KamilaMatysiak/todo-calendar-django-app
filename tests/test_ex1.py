import pytest
from django.urls import reverse


def test_example():
    assert 1 == 1

"""
@pytest.mark.django_db
def test_home_view(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200

"""
