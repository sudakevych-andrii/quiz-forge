from django.urls import reverse
from rest_framework.test import APIClient


def test_health(api_client: APIClient) -> None:
    response = api_client.get(reverse("health"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_schema_and_docs_are_public(api_client: APIClient) -> None:
    assert api_client.get(reverse("schema")).status_code == 200
    assert api_client.get(reverse("docs")).status_code == 200
