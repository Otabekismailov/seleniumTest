import pytest

from apps.account.models import OneTimePass, Notification, CustomPermission, Role
from core.utils import tools
from core.utils.constants import CONSTANTS


# pytestmark = pytest.mark.
class TestOneTimePass:

    @pytest.mark.django_db
    def test_one_time_pass_str(self):
        one = OneTimePass.objects.create(username="test", type=tools.CONSTANTS.ConfirmType.LOGIN, cycle=1)
        assert one.__str__() == f'{one.hash}'
        one.confirm()
        assert one.cycle == 2


class TestNotification:
    @pytest.mark.django_db
    def test_notification(self):
        notification = Notification.objects.create(text="test", phone="+998913498575", type='sms', status='success')
        assert notification.__str__() == f'{notification.get_type_display()}: {notification.phone}'


class TestRole:

    def test_role_str(self, new_role):
        role = new_role.create()

        assert role.__str__() == f"{role.id}-{role.name}"

    def test_role_create_roles(self, new_role):
        Role.create_roles()
        new_ = [role.name for role in Role.objects.all()]
        assert sorted(CONSTANTS.StaffRole.LIST) == sorted(new_)
        assert Role.create_roles() is None

    def test_get_role(self, new_role):
        role = new_role.create()

        role.create_roles()
        getRole = role.get_role('owner')

        assert getRole.name == 'owner'
        assert getRole is not None


class TestCustomPermission:

    def test_permission_str(self, new_permissions):
        permission = new_permissions.create()
        assert permission.__str__() == ' -> '.join(permission.get_all_parent_codes())

    def test_permission_true_or_false(self, new_permissions, new_role):
        role = new_role.create(name="role")
        permission_is_true = new_permissions.create(name="test0", permission_code="testcode.0", )
        permission_is_false = new_permissions.create(name="test1", permission_code="testcode.1", )
        role.permissions.add(permission_is_true)
        perm_is_true = permission_is_true.__class__.objects.filter(id=permission_is_true.id)
        perm_is_false = permission_is_false.__class__.objects.filter(id=permission_is_false.id)
        is_true = permission_is_true.as_dict(perm_is_true, role)
        is_false = permission_is_false.as_dict(perm_is_false, role)
        assert {permission_is_true.permission_code.split(".")[-1]: True} == is_true
        assert {permission_is_false.permission_code.split(".")[-1]: False} == is_false

    def test_permission_child_false(self, new_permissions, new_role):
        role = new_role.create(name="role")
        permission = new_permissions.create(name="test0", permission_code="testcode.0", )
        permission_2 = new_permissions.create(name="test2", permission_code="testcode.2", parent=permission)
        role.permissions.add(permission)
        assert permission.as_dict(permission.__class__.objects.filter(id=permission.id), role) == {
            permission.permission_code.split(".")[-1]: {permission_2.permission_code.split(".")[-1]: False}}

    def test_permission_child_true(self, new_permissions, new_role):
        role = new_role.create(name="role")
        permission = new_permissions.create(name="test0", permission_code="testcode.0", )
        permission_2 = new_permissions.create(name="test2", permission_code="testcode.2", parent=permission)
        role.permissions.add(permission, permission_2)
        assert permission.as_dict(permission.__class__.objects.filter(id=permission.id), role) == {
            permission.permission_code.split(".")[-1]: {permission_2.permission_code.split(".")[-1]: True}}

    def test_permission_not_true(self, new_permissions, new_role):
        role = new_role.create(name="role")
        permission = new_permissions.create(name="test0", permission_code="testcode.0", parent=None)

        role.permissions.add(permission)
        assert permission.as_dict(None, role) == {permission.permission_code.split(".")[-1]: True}

    def test_permission_not_false(self, new_permissions, new_role):
        role = new_role.create(name="role")
        permission = new_permissions.create(name="test0", permission_code="testcode.0", parent=None)

        assert permission.as_dict(None, role) == {permission.permission_code.split(".")[-1]: False}

    def test_construct_dict(self, new_role):
        role = new_role.create()
        parent_permission = CustomPermission()
        assert parent_permission.as_dict([], role) == {}


# class
