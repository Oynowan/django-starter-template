import pytest
from apps.user.models import CustomUser

@pytest.fixture
def user_1(db):
    return CustomUser.objects.create(email='user@test.com', first_name="User", last_name="Test")

@pytest.mark.django_db
def test_user_get_full_name(user_1):
    assert user_1.get_full_name() == 'User Test'