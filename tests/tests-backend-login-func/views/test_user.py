import pytest
from django.db import connection
from django.urls import reverse

from apps.account.models import Merchant
from apps.public.models import DeepenVersion


class TestUserViews:


    def test_user_register_valid(self, api_client, setup_merchant_user):
        header = {"Accept-Language": "uz"}
        data = {"email": "Ismailov@gmail.com", "password": "12345678i", "phone": "1234567890"}
        url = reverse("user:user-register")
        response = api_client.post(url, data, format="json", **header)
        assert response.status_code == 200
        assert response.data["success"] is True
        assert response.data["message"] == "OK"

    def test_user_register_email_invalid(self, api_client, setup_merchant_user):
        header = {"Accept-Language": "uz"}
        data = {"email": "Ismailovgmail.com", "password": "12345678i", "phone": "1234567890"}
        url = reverse("user:user-register")
        response = api_client.post(url, data, format="json", **header)
        assert response.status_code == 400
        assert response.data["message"] == 'email: Enter a valid email address.'
        assert response.data["success"] == False

    def test_user_register_phone_invalid(self, api_client, setup_merchant_user):
        header = {"Accept-Language": "uz"}
        data = {"email": "Ismailov@gmail.com", "password": "12345678i", "phone": ""}
        url = reverse("user:user-register")
        response = api_client.post(url, data, format="json", **header)
        assert response.status_code == 400
        assert response.data["message"] == 'phone: This field may not be blank.'
        assert response.data["success"] == False

    def test_user_verify_valid(self, api_client, setup_merchant_user, verification):
        user = setup_merchant_user
        user.username = "+1234567890"
        user.phone = "+1234567890"
        user.save()
        ver = verification.create(user=user, code_type='register', code=222222,
                                  expires_at='2025-08-12 07:17:41.332162 +00:00')
        data = {
            "phone": user.phone,
            "code": ver.code
        }
        url = reverse("user:verify-account")
        response = api_client.post(url, data, format="json")
        assert response.data["success"] is True
        assert response.data["message"] == "OK"
        assert response.status_code == 200

    def test_user_verify_invalid__blank_phone(self, api_client, setup_merchant_user, verification):
        user = setup_merchant_user
        user.username = "+1234567890"
        user.phone = "+1234567890"
        user.save()
        ver = verification.create(user=user, code_type='register', code=222222,
                                  expires_at='2025-08-12 07:17:41.332162 +00:00')
        data = {
            "phone": '',
            "code": ver.code
        }
        url = reverse("user:verify-account")
        response = api_client.post(url, data, format="json")
        assert response.data["success"] is False
        assert response.data["message"] == "phone: This field may not be blank."
        assert response.status_code == 400

    def test_user_verify_invalid_phone_false(self, api_client, setup_merchant_user, verification):
        user = setup_merchant_user
        user.username = "+1234567890"
        user.phone = "+1234567890"
        user.save()
        ver = verification.create(user=user, code_type='register', code=222222,
                                  expires_at='2025-08-12 07:17:41.332162 +00:00')
        data = {
            "phone": '+123456789',
            "code": ver.code
        }
        url = reverse("user:verify-account")
        response = api_client.post(url, data, format="json")
        assert response.data["success"] is False
        assert response.data["message"] == "detail: User not found"
        assert response.status_code == 400

    def test_user_verify_invalid_code_blank(self, api_client, setup_merchant_user, verification):
        user = setup_merchant_user
        user.username = "+1234567890"
        user.phone = "+1234567890"
        user.save()
        ver = verification.create(user=user, code_type='register', code=222222,
                                  expires_at='2025-08-12 07:17:41.332162 +00:00')
        data = {
            "phone": '+1234567890',
            "code": ''
        }
        url = reverse("user:verify-account")
        response = api_client.post(url, data, format="json")
        assert response.data["success"] is False
        assert response.data["message"] == 'code: A valid integer is required.'
        assert response.status_code == 400

    def test_user_verify_invalid_code_false(self, api_client, setup_merchant_user, verification):
        user = setup_merchant_user
        user.username = "+1234567890"
        user.phone = "+1234567890"
        user.save()
        ver = verification.create(user=user, code_type='register', code=222222,
                                  expires_at='2025-08-12 07:17:41.332162 +00:00')
        data = {
            "phone": '+1234567890',
            "code": '12313'
        }
        url = reverse("user:verify-account")
        response = api_client.post(url, data, format="json")
        assert response.data["success"] is False
        assert response.data["message"] == 'code: Invalid code'
        assert response.status_code == 400
