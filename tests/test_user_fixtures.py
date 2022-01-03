import pytest
from users.models import User

user_data = {
    'username': 'Adam Osiowy',
    'email': 'addammmm@o2.pl',
    'password': 'dsfgfgggf22234@$sa',
}


@pytest.fixture
def user1(db):
    return User.objects.create_user(**user_data)

@pytest.mark.django_db
def test_password(user2):
    assert user2.password == '12345dsfeggggg'

@pytest.mark.django_db
def test_user_count(user1):
    assert User.objects.all().count() == 1


@pytest.mark.django_db
def test_username(user1):
    assert user1.username == user_data['username']


@pytest.mark.django_db
def test_email(user1):
    assert user1.email == user_data['email']
