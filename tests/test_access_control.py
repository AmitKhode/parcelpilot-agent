import pytest
from app.security.access_control import authorize, AuthorizationError

def test_customer_allowed_own_data():
    user = {"role": "CUSTOMER", "account_id": "ACCT-001"}
    assert authorize(user, resource_account_id="ACCT-001") is True

def test_customer_denied_other_data():
    user = {"role": "CUSTOMER", "account_id": "ACCT-002"}
    with pytest.raises(AuthorizationError):
        authorize(user, resource_account_id="ACCT-001")

def test_support_agent_allowed_all_data():
    user = {"role": "SUPPORT_AGENT", "account_id": None}
    assert authorize(user, resource_account_id="ACCT-001") is True
    assert authorize(user, resource_account_id="ACCT-002") is True