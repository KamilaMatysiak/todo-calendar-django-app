import pytest
from users.models import User
from users.models import UserProfile

@pytest.mark.django_db
def test_user_create():
    user = User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa')
    UserProfile.objects.create(user=user, firstname="Adam Osiowy", birthdate="1977-05-03", phonenumber="123435634")

    assert UserProfile.objects.count() >= 1


@pytest.mark.django_db
def test_username():
    user = User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa')
    userprofile = UserProfile.objects.create(user=user, firstname="Adam Osiowy", birthdate="1977-05-03",
                                             phonenumber="123435634")

    assert userprofile.firstname == user.username and userprofile.firstname == "Adam Osiowy"


@pytest.mark.django_db
def test_birthdate():
    user = User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa')
    userprofile = UserProfile.objects.create(user=user, firstname="Adam Osiowy", birthdate="1977-05-03",
                                             phonenumber="123435634")

    assert userprofile.birthdate == "1977-05-03"


@pytest.mark.django_db
def test_phonenumber():
    user = User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa')
    userprofile = UserProfile.objects.create(user=user, firstname="Adam Osiowy", birthdate="1977-05-03",
                                             phonenumber="123435634")

    assert userprofile.phonenumber == "123435634"


@pytest.mark.django_db
def test_unique():
    user1 = User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa')
    userprofile1 = UserProfile.objects.create(user=user1, firstname="Adam Osiowy", birthdate="1977-05-03",
                                              phonenumber="123435634")

    user2 = User.objects.create_user('Grzegorz Nowak', 'grzegorznowak12@gmail.com', '12345dsfeggggg')
    userprofile2 = UserProfile.objects.create(user=user2, firstname="Grzegorz Nowak", birthdate="1937-04-11",
                                              phonenumber="933356545")
    assert user1 is not user2 and userprofile1 is not userprofile2
