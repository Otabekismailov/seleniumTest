import pytest
from django.db import connection
from django_tenants.utils import get_tenant_model

from apps.account.models import Merchant

pytest_db = pytest.mark.django_db

tenant_model = get_tenant_model()


class TestMerchantModel:

    def test_str_return(self, merchant_tn):
        connection.set_schema_to_public()
        mr = merchant_tn.create()

        assert mr.__str__() == mr.merchant_name
        assert mr.get_owner() == mr.merchant_users.first()

    @pytest.mark.django_db
    def test_get_tenant(self):
        connection.set_schema_to_public()
        merchant_tn = Merchant.objects.create(merchant_name="otabek", merchant_address="namangan", subdomain="test",
                                              phone="+998913489575")
        assert merchant_tn.get_tenant().schema_name == merchant_tn.subdomain

    def test_get_tenant_none(self, merchant_tn):
        connection.set_schema_to_public()
        merchant = merchant_tn.create(subdomain="")

        tenant = merchant.get_tenant()

        assert tenant is None
