import pytest

from apps.account.manager import UserManager, UserUniqueIdentifierChecker
from apps.account.models import Merchant, User, Role, CustomPermission
from apps.fitness.models import Club
from apps.staff.models import ClubStaff
from core.api.exceptions import UserNotVerified, CustomValidationError
from core.utils import tools

pytest_db = pytest.mark.django_db


class TestUserManager:
    @pytest.mark.django_db
    def test_create_user_not_username(self):
        UserManager()
        error_message = 'The given username must be set'

        # Check that ValueError is raised with the expected message
        with pytest.raises(ValueError, match=error_message):
            User.objects._create_user(
                username="", first_name="Test", last_name="User", email="tests@example.com", phone="+998913489575",
                password="testpassword"
            )

    @pytest.mark.django_db
    def test_create_user_not_phone(self):
        UserManager()
        error_message = 'Either email or phone number must be set'

        # Errorlarnga test yozish uchun expmle
        with pytest.raises(ValueError, match=error_message):
            User.objects._create_user(
                username="Otabek", first_name="Test", last_name="User", email="", phone="",
                password="testpassword",
                auth_method="email",
            )

    @pytest.mark.django_db
    def test_create_user_not_auth(self):
        UserManager()
        error_message = 'Auth method must be set'

        with pytest.raises(ValueError, match=error_message):
            User.objects._create_user(
                username="Otabek", first_name="Test", last_name="User", email="test@gmail.com", phone="+998913489575",
                password="testpassword"
            )

    @pytest.mark.django_db
    def test_create_user_create_uni(self):
        UserManager()
        user = User.objects.create_user(
            first_name="Test", last_name="User", email="test@example.com",
            phone="1234567890", password="testpassword", is_verified=True, auth_method="email", user_type='staff'
        )

        with pytest.raises(CustomValidationError, match=f'User with username: {user.username} already exists'):
            User.objects.create_user(
                first_name="Test", last_name="User", email="test@example.com",
                phone="1234567890", password="testpassword", is_verified=True, auth_method="email", user_type='staff'
            )

    @pytest.mark.django_db
    def test_create_user_create_ver(self):
        UserManager()
        User.objects.create_user(

            first_name="Test", last_name="User", email="test@example.com",
            phone="1234567890", password="testpassword", auth_method="email", user_type='customer'
        )

        with pytest.raises(UserNotVerified, match=f'User not verified'):
            User.objects.create_user(

                first_name="Test", last_name="User", email="test@example.com",
                phone="1234567890", password="testpassword", auth_method="email", user_type='customer',
            )

    def test_user_type(self, user_manager):
        user_type_is_false = tools.CONSTANTS.UserType.CUSTOMER
        user_type_is_true = tools.CONSTANTS.UserType.STAFF
        assert user_manager._get_is_verified(user_type_is_false) is False
        assert user_manager._get_is_verified(user_type_is_true) is True

    def test_use_validate_user_input(self, user_manager):
        owner = tools.CONSTANTS.UserType.OWNER
        staff = tools.CONSTANTS.UserType.STAFF
        with pytest.raises(CustomValidationError, match=f"Both email and phone number must be set for {owner}"):
            user_manager._validate_user_input(owner, None, None)
        with pytest.raises(CustomValidationError, match=f'Email must be set for {staff}'):
            user_manager._validate_user_input(staff, None, "+998913489575")

    @pytest.mark.django_db
    def test_create_user_create_not_email_or_phone(self):
        UserManager()
        user_not_email = User.objects.create_user(
            first_name="Test", last_name="User",
            phone="1234567890", password="testpassword", auth_method="email", user_type='customer'
        )
        user_not_phone = User.objects.create_user(

            first_name="Test", last_name="User",
            email="test@exampe.com", password="testpassword", auth_method="email", user_type='staff'
        )
        assert user_not_email.username.__str__() == "1234567890"
        assert user_not_phone.username.__str__() == "test@exampe.com"

    @pytest.mark.django_db
    def test_create_user_create_super_user(self):
        UserManager()

        user = User.objects.create_superuser(
            username="test",
            email="test@example.com",
            first_name="Test", last_name="User",
            phone="1234567890", password="testpassword",
        )
        assert user.is_superuser is True
        assert user.is_staff is True

    @pytest.mark.django_db
    def test_get_staff(self, user_manager):
        merchant = Merchant.objects.create(merchant_name="otabek", merchant_address="admin@localhost",
                                           subdomain="test",
                                           phone="+998913499575")
        user = User.objects.create_user(

            first_name="Test", last_name="User", email="test@exampe.com",
            phone="1234567890", password="testpassword", auth_method="email", user_type='staff', merchant=merchant
        )
        user_2 = User.objects.create_user(

            first_name="Test", last_name="User", email="test@exape.com",
            phone="1234567890", password="testpassword", auth_method="email", user_type='owner', )

        assert user.__class__.objects.get_staffs(merchant.id) is not None
        assert user_2.__class__.objects.get_staffs(1234).first() is None

    @pytest.mark.django_db
    def test_filter_active(self, user_manager):
        user = User.objects.create_user(

            first_name="Test", last_name="User", email="test@exampe.com",
            phone="1234567890", password="testpassword", auth_method="email", user_type='staff', is_active=True,
        )
        assert user.__class__.objects.filter_active() is not None

    @pytest.mark.django_db
    def test_get_all_trainer(self, user_manager):
        user = User.objects.create_user(

            first_name="Test", last_name="User", email="test@exampe.com",
            phone="1234567890", password="testpassword", auth_method="email",
            user_type='staff',
        )
        mr = Merchant.objects.create(merchant_name="otabek", merchant_address="admin@localhost", subdomain="test",
                                     phone="+998913499575")
        merchant = User.objects.create_user(

            first_name="Tes",
            last_name="Use",
            email="test@example.com",
            phone="+998913499577",
            password="testpassword",
            auth_method="email",
            user_type="owner",
            merchant=mr,
        )
        permission = CustomPermission.objects.create(name="staff", permission_code="admin")
        role = Role.objects.create(name=tools.CONSTANTS.StaffRole.TRAINER, title="user")

        role.permissions.add(permission)
        club = Club.objects.create(mr=mr, name="Club 1", phone="+998913499575", merchant=merchant)
        club_staff = ClubStaff.objects.create(staff=user, role=role, club=club, is_selected=True)
        assert user.__class__.objects.get_trainers(club.id) is not None


class TestUserUniqueIdentifierChecker:
    @pytest.mark.django_db
    def test_unique_email(self):
        user = User.objects.create_user(

            first_name="Test", last_name="User", email="test@exampe.com",
            phone="1234567890", password="testpassword", auth_method="email",
            user_type='staff',
        )

        assert UserUniqueIdentifierChecker(email=user.email,
                                           phone=user.phone, ).is_email_unique() is False
        assert UserUniqueIdentifierChecker(email="ismailov1995@gmail.com",
                                           phone="+998913489575", ).is_email_unique() is True

    @pytest.mark.django_db
    def test_unique_phone(self):
        user = User.objects.create_user(

            first_name="Test", last_name="User", email="test@exampe.com",
            phone="1234567890", password="testpassword", auth_method="email",
            user_type='staff',
        )
        assert UserUniqueIdentifierChecker(email=user.email,
                                           phone=user.phone, ).is_phone_unique() is False
        assert UserUniqueIdentifierChecker(email="ismailov1995@gmail.com",
                                           phone="+998913489572", ).is_phone_unique() is True

    @pytest.mark.django_db
    def test_unique_phone_and_email(self):
        user = User.objects.create_user(

            first_name="Test", last_name="User", email="test@exampe.com",
            phone="1234567890", password="testpassword", auth_method="email",
            user_type='staff',
        )
        assert UserUniqueIdentifierChecker(email=user.email,
                                           phone=user.phone, ).is_email_and_phone_unique() is False
        assert UserUniqueIdentifierChecker(email="ismailov1995@gmail.com",
                                           phone="+998913489572", ).is_email_and_phone_unique() is True
