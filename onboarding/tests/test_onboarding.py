from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
class TestOnboarding:

    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.get('/api/v1/onboarding/user_answer/next-question/', data={})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # def test_if_user_is_authenticated_returns_200(self, user):
    #     client = APIClient()
    #     client.force_authenticate(user=user)
    #     response = client.get('/api/v1/onboarding/user_answer/next-question/', data={})
    #     assert response.status_code == status.HTTP_200_OK
