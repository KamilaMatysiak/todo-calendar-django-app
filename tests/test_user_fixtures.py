import pytest
from users.models import User
from tasks.models import Task

@pytest.fixture
def user1(db):
    return User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa')



@pytest.mark.django_db
def test_username(user1):
    assert user1.username == 'Adam Osiowy'
