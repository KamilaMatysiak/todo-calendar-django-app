import pytest
from users.models import User

"""@pytest.fixture
def user1(db):
    return User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa')
@pytest.fixture
def user2(db):
    return User.objects.create_user('Grzegorz Nowak', 'grzegorznowak12@gmail.com', '12345dsfeggggg')




@pytest.mark.django_db
def test_username(user2):
    assert user2.username == 'Grzegorz Nowak'


@pytest.mark.django_db
def test_mail(user2):
    assert user2.email == 'grzegorznowak12@gmail.com'


@pytest.mark.django_db
def test_password(user2):
    assert user2.password == '12345dsfeggggg'


@pytest.mark.django_db
def test_unique(user1, user2):
    assert user1 is not user2
"""