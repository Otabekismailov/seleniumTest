import pytest
from rest_framework.exceptions import ValidationError

from apps.account.api.serializers import VerifyAccountSerializer, LoginMerchantSerializer, RedirectMerchantSerializer, \
    UniqueUserIdentifierMixin, StaffProfileSerializer, EmailPhoneBaseSerializer, UserRegistrationSerializer
from apps.account.models import OneTimePass, User
from core.api.exceptions import CustomValidationError


class TestLoginMerchantSerializer:
    @pytest.fixture
    def setup_user(self, new_user):
        user_data = {
            'username': 'test@example.com',
            'password': '1234',
            'merchant_name': 'Test Merchant',
            'merchant_phone': '1234567890',
            'merchant_address': '123 Test Street',
            'staff_name': 'John Doe',
            'staff_phone': '0987654321',
        }
        user = new_user.create(**user_data)
        user.set_password(user_data['password'])
        user.save()
        return user

    def test_serializer_valid_credentials(self, setup_user):
        data = {'username': 'test@example.com',
                'password': '1234', }

        serializers = LoginMerchantSerializer(data=data)
        serializers.is_valid(raise_exception=True)
        assert serializers.is_valid()
        assert sorted(serializers.data.keys()) == sorted(['username'])

    def test_login_serializer_invalid_credentials(self, setup_user):
        data = {'username': 'test@example.com',
                'password': '123', }
        with pytest.raises(CustomValidationError, match="Incorrect authentication credentials.") as exp:
            serializers = LoginMerchantSerializer(data=data)
            serializers.is_valid(raise_exception=True)

        assert str(exp.value) == 'Incorrect authentication credentials.'

    def test_login_serializer_filed_blank(self, setup_user):
        data = {
            'username': '',
            'password': '',
        }

        serializer = LoginMerchantSerializer(data=data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors
        assert 'password' in serializer.errors


class TestRedirectMerchantSerializer:
    @pytest.fixture
    def setup_redirect(self, db):
        data = {
            "username": "test@example",
            "type": "login", "cycle": 1}
        qs = OneTimePass.objects.create(**data)
        return qs

    def test_serializer_valid_redirect_merchant(self, setup_redirect):
        data = {'hash': setup_redirect.hash, }

        serializer = RedirectMerchantSerializer(data=data)
        if serializer.is_valid():
            assert serializer.data == {}

    def test_serializer_invalid_redirect_merchant(self, setup_redirect):
        data = {'hash': "1233322826e0P6yGfhISpIw3jG"}
        with pytest.raises(CustomValidationError, match="Invalid OTP") as exp:
            serializer = RedirectMerchantSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        assert str(exp.value) == "Invalid OTP"


class TestUniqueUserIdentifierMixin:

    def test_identifier_valid(self, new_user):
        new_user.create(username='test@example', phone="+998913499575", auth_method="email")
        check = UniqueUserIdentifierMixin()
        check.validate_unique_user('test@exampl', "998913499576", "phone")

    def test_identifier_invalid(self, new_user):
        new_user.create(username='test@example', phone="+998913499575", auth_method="phone")
        check = UniqueUserIdentifierMixin()
        with pytest.raises(CustomValidationError, match="User with this phone number or email already exists") as exp:
            check.validate_unique_user('test@example', "+998913499575", "email")

        assert str(exp.value) == "User with this phone number or email already exists"


class TestStaffProfileSerializer:

    def test_staff_profile_serializer_valid(self, setup_db):
        user, role, club, merchant, club_staff = setup_db
        serializers = StaffProfileSerializer(user)
        assert isinstance(serializers.data['avatar'], dict)
        assert serializers.data['avatar'] is not None
        assert sorted(serializers.data.keys()) == sorted(
            ['first_name', 'last_name', 'gender', 'birth_date', 'phone', 'email', 'avatar', 'role'])

    def test_staff_profile_serializer_avatar_none(self, setup_db):
        user, role, club, merchant, club_staff = setup_db
        user.avatar = None
        user.save()
        serializers = StaffProfileSerializer(user)
        assert serializers.data['avatar'] is None
        assert sorted(serializers.data.keys()) == sorted(
            ['first_name', 'last_name', 'gender', 'birth_date', 'phone', 'email', 'avatar', 'role'])

    def test_staff_profile_serializer_validate_invalid(self, new_user):
        user = new_user.create(email="my@gmail.com")
        data = {"email": "m@gmail.com"}
        with pytest.raises(CustomValidationError, match="Email can not be updated") as exp:
            serializers = StaffProfileSerializer(user, data=data, partial=True)
            serializers.is_valid(raise_exception=True)
        assert str(exp.value) == "Email can not be updated"

    def test_staff_profile_serializer_validate_valid(self, setup_db):
        user, role, club, merchant, club_staff = setup_db
        data = {"email": user.email, "first_name": "Jon"}
        serializers = StaffProfileSerializer(user, data=data, partial=True)
        serializers.is_valid(raise_exception=True)
        assert sorted(serializers.data.keys()) == sorted(
            ['first_name', 'last_name', 'gender', 'birth_date', 'phone', 'email', 'avatar', 'role'])


class TestEmailPhoneBaseSerializer:
    def test_email_phone_base_serializer_valid(self, db):
        data = {
            "email": "otabek@gmail.com",
            "phone": "+4444444444"
        }
        serializer = EmailPhoneBaseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        assert sorted(serializer.data.keys()) == sorted(['email', 'phone'])
        assert serializer.data is not None

    def test_email_phone_base_serializer_invalid(self, db):
        data = {
            "email": "otabek@gmail.com",

        }
        with pytest.raises(ValidationError, match="Phone number must be set") as exp:
            serializer = EmailPhoneBaseSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        assert exp.value.detail['error'] == ["Phone number must be set"]


class TestUserRegistrationSerializer:

    def test_valid(self, db):
        data = {
            "phone": "+998913489575",
            "password": "12345678i",
        }
        serializer = UserRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        assert sorted(serializer.data.keys()) == sorted(['email', 'phone'])

    def test_invalid(self, db):
        user = User.objects.create(
            username="+998913489575",
            first_name="Test", last_name="User", email="test@example.com",
            phone="+998913489575", password="testpassword", auth_method="phone", type='customer'
        )
        data = {
            "username": user.phone,
            "email ": user.email,
            "phone": user.phone,
            "password": user.password,

        }
        serializer = UserRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        assert sorted(serializer.data.keys()) == sorted(['email', 'phone'])


class TestVerifyAccountSerializer:

    def test_invalid_user_not_found(self, db):
        data = {
            "email ": "otabek@gmail.com",
            "phone": "998913489575",
            "code": 123345,

        }
        with pytest.raises(CustomValidationError, match="User not found") as excinfo:
            serializer = VerifyAccountSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        assert str(excinfo.value) == "User not found"

    def test_invalid_user_verified(self, new_user):
        user = new_user.create(username="+998913489575",
                               first_name="Test", last_name="User", email="test@example.com",
                               phone="+998913489575", password="testpassword", auth_method="phone", type='customer')
        user.verify()
        data = {
            "phone": user.phone,
            "code": 12344,
        }
        with pytest.raises(CustomValidationError, match="User already verified") as excinfo:
            serializer = VerifyAccountSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        assert str(excinfo.value) == "User already verified"

    def test_valid_user_verified(self, new_user, verification):
        user = new_user.create(username='+998913489575', password='12345678i', auth_method='phone',
                               phone="+998913489575")
        ver = verification.create(user=user, code_type='register', code=222222,
                                  expires_at='2025-08-12 07:17:41.332162 +00:00')
        data = {
            "phone": user.phone,
            "code": ver.code
        }
        serializer = VerifyAccountSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        assert sorted(serializer.data.keys()) == sorted(['email', 'phone'])
