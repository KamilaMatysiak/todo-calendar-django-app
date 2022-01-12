import pytest
from users.models import User
from calendar_app.models import Meeting


@pytest.fixture
def user1(db):
    return User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa', id=1)


@pytest.fixture
def user2(db):
    return User.objects.create_user('Grzegorz Nowak', 'grzegorznowak12@gmail.com', '12345dsfeggggg')


@pytest.fixture
def meeting1(user1):
    return Meeting.objects.create(title="Naprawić błąd połączenia", description="Strona nie zawsze się ładuje")


@pytest.mark.django_db
def test_meeting(user1, meeting1):
    assert meeting1.title == "Naprawić błąd połączenia" and meeting1.description == "Strona nie zawsze się ładuje"


@pytest.fixture
def meeting2(user1):
    return Meeting.objects.create(title="Sprawdzić odległość na mapie", description="Zadania powinny wyświetlać się, "
                                                                                    "gdy użytkownik jest blisko",
                                  color="red", l_lat=52.3992806, l_lon=16.9199655)


def test_latitude_and_longitude(user1, meeting2):
    assert meeting2.title == "Sprawdzić odległość na mapie" \
           and meeting2.l_lat == 52.3992806 and meeting2.l_lon == 16.9199655
