import pytest
from users.models import User
from tasks.models import Task

@pytest.fixture
def user1(db):
    return User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa', id=1)

@pytest.fixture
def user2(db):
    return User.objects.create_user('Grzegorz Nowak', 'grzegorznowak12@gmail.com', '12345dsfeggggg')


@pytest.mark.django_db
def test_task():
    #title, localization, l_lat, l_lon, with_who, date, time, priorirty, complete, created, accepted, category_id, from_who_id, meeting_id, user_id
    Task.objects.create(title="Spotkanie z przełożonym", priority="N", accepted=1, user_id=1)
    assert Task.objects.count() >= 1
