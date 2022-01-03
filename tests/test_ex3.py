import pytest
from users.models import User
from users.models import UserProfile


@pytest.mark.django_db
def test_user_create():
    print("Raz")
    user = User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa')
    UserProfile.objects.create(user=user, firstname="Adam Osiowy", birthdate="1977-05-03", phonenumber="123435634")

    assert UserProfile.objects.count() >= 1


"""
@pytest.mark.django_db
def test_username():
    UserProfile.objects.create_user('Grzegorz Nowak', 'grzegorznowak12@gmail.com', '12345dsfeggggg')
    me = UserProfile.objects.get(username='Grzegorz Nowak')
    assert me.username == 'Grzegorz Nowak'


@pytest.mark.django_db
def test_unique():
    user1 = UserProfile.objects.create_user('Grzegorz Nowak', 'grzegorznowak12@gmail.com', '12345dsfeggggg')
    user2 = UserProfile.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa')
    assert user1 is not user2
"""
