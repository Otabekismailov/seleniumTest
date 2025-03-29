import pytest
from django.conf import settings

from apps.account.models import Merchant, User, Role, CustomPermission
from apps.fitness.models import Club
from apps.staff.models import ClubStaff
from core.api.exceptions import CustomValidationError
from core.utils import db, tools
from core.utils.constants import CONSTANTS

pytest_db = pytest.mark.django_db


class TestUserModel:

    @pytest.mark.django_db
    def test_create_user(self, user_manager):
        user = User.objects.create_user(

            first_name="Test",
            last_name="User",
            email="tests@example.com",
            phone="+998913499575",
            password="testpassword",
            auth_method="email",
            user_type="staff"
        )

        assert isinstance(user, User)
        assert user.email == "tests@example.com"
        assert user.phone == "+998913499575"
        assert user.auth_method == "email"
        assert user.type == "staff"


    def test_create_user_str(self, new_user):
        user = new_user.create()

        assert isinstance(user, User)
        assert user.__str__() == f"{user.id}: {user.username}"

    def test_get_full_name(self, new_user):
        user = new_user.create()
        assert user.get_full_name() == f"{user.first_name} {user.last_name}"


    def test_get_short_name(self, new_user):
        user = new_user.create()
        assert user.get_short_name() == f"{user.first_name}"


    def test_has_perm_true(self, new_user):
        user = new_user.create()

        assert user.has_perm("owner") is True


    def test_has_perm_false(self, new_user):
        user = new_user.create()
        with pytest.raises(CustomValidationError, match="Staff is not a member of any club"):
            user.has_perm("staff.")


    def test_has_custom_perm_true(self, new_user):
        user = new_user.create()
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
        role = Role.objects.create(name="admin", title="user")

        role.permissions.add(permission)
        club = Club.objects.create(mr=mr, name="Club 1", phone="+998913499575", merchant=merchant)
        club_staff = ClubStaff.objects.create(staff=user, role=role, club=club, is_selected=True)

        has_perm = user.has_custom_perm("staff.admin")
        assert has_perm is True

        role.permissions.remove(permission)
        has_perm = user.has_custom_perm("staff.admin")
        assert has_perm is False

    @pytest.mark.django_db
    def test_get_role(self, user_manager, new_user):
        user = new_user.create(type="owner")
        mr = Merchant.objects.create(merchant_name="otabek", merchant_address="admin@localhost", subdomain="test",
                                     phone="+998913499573")
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
        permission = CustomPermission.objects.create(name="staff", permission_code="owner")
        role = Role.objects.create(name='admin', title="user")

        club = Club.objects.create(mr=mr, name="Club 1", phone="+998913499575", merchant=merchant)
        club_staff = ClubStaff.objects.create(staff=user, role=role, club=club, is_selected=True)

        assert user.get_role() == db.Role.objects.filter(name=CONSTANTS.StaffRole.OWNER).first()

    @pytest.mark.django_db
    def test_get_permissions_as_dict(self, user_manager, new_user):
        user = new_user.create(type="owner")
        mr = Merchant.objects.create(merchant_name="otabek", merchant_address="admin@localhost", subdomain="test",
                                     phone="+998913499573")
        merchant = User.objects.create_user(

            first_name="Tes",
            last_name="Use",
            email="test@example.com",
            phone="+998913499577",
            password="testpassword",
            auth_method="email",
            user_type=tools.CONSTANTS.UserType.OWNER,
            merchant=mr,
        )
        permission = CustomPermission.objects.create(name="gym", permission_code="owner", parent=None)
        role = Role.objects.create(name=tools.CONSTANTS.StaffRole.TRAINER, title="user")

        role.permissions.add(permission)
        club = Club.objects.create(mr=mr, name="Club 1", phone="+998913499575", merchant=merchant)
        club_staff = ClubStaff.objects.create(staff=user, role=role, club=club, is_selected=True)
        assert isinstance(user.get_permissions_as_dict(), dict)

    @pytest.mark.django_db
    def test_full_name(self, user_manager, new_user):
        user = new_user.create()

        assert user.full_name() == f"{user.first_name} {user.last_name}"

    @pytest.mark.django_db
    def test_avatar(self, user_manager, new_user):
        user = new_user.create()

        assert user.get_avatar() == {"id": user.avatar.id, "url": settings.BASE_URL + user.avatar.file.url}
        user_2 = new_user.create(username="odil", email="oo@gmail.com", phone="+998913499571")
        user_2.avatar = None
        user_2.save()
        assert user_2.get_avatar() is None

    @pytest.mark.django_db
    def test_verify(self, user_manager, new_user):
        user = new_user.create(is_verified=False)
        user.verify()
        assert user.is_verified is True

    @pytest.mark.django_db
    def test_is_owner(self, user_manager, new_user):
        user = new_user.create(type=tools.CONSTANTS.UserType.OWNER)

        assert user.is_owner() is True

    @pytest.mark.django_db
    def test_delete(self, user_manager, new_user):
        user = new_user.create()
        username = user.username

        user.delete()
        times = user.deleted_at.timestamp()
        assert user.username == f"{username}-{int(times)}"

    @pytest.mark.django_db
    def test_before_save(self, user_manager, new_user):
        not_phone = new_user.create(email="oo@gmail.com", auth_method='', phone='')
        not_email = new_user.create(username='prif', email='', auth_method='', phone='+9988913499571')
        or_email = new_user.create(username='email', phone='+9988913499521', email="ooa@gmail.com", auth_method='')
        not_phone.before_save()
        not_email.before_save()
        or_email.before_save()
        assert or_email.has_module_perms("baribir true") is True
        assert or_email.auth_method == tools.CONSTANTS.AUTH_METHOD.EMAIL
        assert not_email.auth_method == tools.CONSTANTS.AUTH_METHOD.PHONE
        assert not_phone.auth_method == tools.CONSTANTS.AUTH_METHOD.EMAIL

    @pytest.mark.django_db
    def test_not_username(self, user_manager, new_user):
        not_username_add_email = new_user.create(username='', email="test@gmail.com",
                                                 auth_method=tools.CONSTANTS.AUTH_METHOD.EMAIL,
                                                 phone='+998912222222')

        not_username_add_phone = new_user.create(username='', email="test@gmail.com",
                                                 auth_method=tools.CONSTANTS.AUTH_METHOD.PHONE,
                                                 phone='+998912222232')

        assert not_username_add_email.username == 'test@gmail.com'
        assert not_username_add_phone.username == "+998912222232"
