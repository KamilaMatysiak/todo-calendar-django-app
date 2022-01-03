"""import pytest
from users.models import User


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa')
    assert User.objects.count() >= 1


@pytest.mark.django_db
def test_username():
    User.objects.create_user('Grzegorz Nowak', 'grzegorznowak12@gmail.com', '12345dsfeggggg')
    me = User.objects.get(username='Grzegorz Nowak')
    assert me.username == 'Grzegorz Nowak'


@pytest.mark.django_db
def test_unique():
    user1 = User.objects.create_user('Grzegorz Nowak', 'grzegorznowak12@gmail.com', '12345dsfeggggg')
    user2 = User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa')
    assert user1 is not user2
"""