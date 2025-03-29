from datetime import timedelta

import pytest
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.account.models import OneTimePass
from core.api.exceptions import CustomValidationError






class TestVerificationCode:

    def test_verification_code(self, verification, new_user):
        user = new_user.create()
        time = timezone.now() + timedelta(
            seconds=int(settings.OTP_SETTINGS['OTP_EXPIRE_TIME'])
        )
        new_ver = verification.create(user=user, expires_at='')

        assert new_ver.expires_at.strftime("%Y-%m-%d %H:%M:%S") == time.strftime("%Y-%m-%d %H:%M:%S")

    def test_verification_create_code(self, verification, new_user):
        user = new_user.create()
        new_ver = verification.create(user=user, code_type='Login', code=12223)
        count = new_ver.__class__.objects.count() + 1
        new_ver.create_code(user, "Login")
        assert new_ver.__class__.objects.count() == count

    def test_send_code(self, verification, new_user):
        user = new_user.create()
        ver = verification.create(user=user, code_type='Login', code=222222,
                                  expires_at='2050-08-14 07:17:41.332162 +00:00')
        with pytest.raises(CustomValidationError, match="Confirmation code already sent, please use that one."):
            ver.send_code(user, "Login")
        ver_2 = verification.create(user=user, code_type='Login', code=222222,
                                    expires_at='2024-08-12 07:17:41.332162 +00:00')

        assert ver_2.already_sent_code(user, "Login") is False

    def test_send_code_delete(self, verification, new_user):
        user = new_user.create(username='test', password='12345678i')
        ver = verification.create(user=user, code_type='Register', code=222222,
                                  expires_at='2024-08-12 07:17:41.332162 +00:00')
        ver.delete_old_codes(user, "Register", exclude_id=ver.id)
        assert ver.__class__.objects.filter(id=ver.id).exists()

    def test_verification_user_register(self, verification, new_user):
        user = new_user.create(username='test', password='12345678i', auth_method='email')
        ver = verification.create(user=user, code_type='register', code=222222,
                                  expires_at='2024-08-12 07:17:41.332162 +00:00')
        with pytest.raises(NotImplementedError):
            ver.send_code(user, "register")

    def test_verification_user_forgot(self, verification, new_user):
        user = new_user.create(username='test', password='12345678i', auth_method='email')
        ver = verification.create(user=user, code_type='forgot', code=222222,
                                  expires_at='2024-08-12 07:17:41.332162 +00:00')
        with pytest.raises(NotImplementedError):
            ver.send_code(user, "forgot")

    def test_verification_user_phone_forget(self, verification, new_user):
        user = new_user.create(username='test', password='12345678i', auth_method='phone', phone="+998913489575")
        ver = verification.create(user=user, code_type='forgot', code=222222,
                                  expires_at='2024-08-12 07:17:41.332162 +00:00')
        with pytest.raises(NotImplementedError):
            ver.send_code(user, "forgot")

    def test_verification_user_phone(self, verification, new_user):
        user = new_user.create(username='test', password='12345678i', auth_method='phone', phone="+998913489575")
        ver = verification.create(user=user, code_type='register', code=222222,
                                  expires_at='2024-08-12 07:17:41.332162 +00:00')
        old_code = ver.__class__.objects.values('id', 'code', 'code_type', 'user').first()
        ver.send_code(user, "register")
        new_code = ver.__class__.objects.values('id', 'code', 'code_type', 'user').last()

        assert sorted([str(old_code['user']), old_code['code_type']]) == sorted(
            [str(new_code['user']), new_code['code_type']])
        assert old_code['id'] != new_code['id']
        assert old_code['code'] != new_code['code']

    def test_verification_code_check_code_invalid(self, verification, new_user):
        user = new_user.create(username='test', password='12345678i', auth_method='phone', phone="+998913489575")
        ver = verification.create(user=user, code_type='register', code=222222,
                                  expires_at='2024-08-12 07:17:41.332162 +00:00')
        with pytest.raises(ValidationError) as excinfo:
            ver.check_code(user, 24444, "register")
        assert excinfo.value.detail == {'code': 'Invalid code'}

    def test_verification_code_check_expires_invalid(self, verification, new_user):
        user = new_user.create(username='test', password='12345678i', auth_method='phone', phone="+998913489575")
        ver = verification.create(user=user, code_type='register', code=222222,
                                  expires_at='2024-08-12 07:17:41.332162 +00:00')
        with pytest.raises(ValidationError) as excinfo:
            ver.check_code(user, 222222, "register")

        assert excinfo.value.detail == {'code': 'Code is expired'}

    def test_verification_code_check(self, verification, new_user):
        user = new_user.create(username='test', password='12345678i', auth_method='phone', phone="+998998118971")
        ver = verification.create(user=user, code_type='register', code=222222,
                                  expires_at='2025-08-12 07:17:41.332162 +00:00')
        ver.check_code(user, 222222, "register")
        counts = ver.__class__.objects.filter(code=222222, user=user, code_type='register').count()
        assert counts == 0
