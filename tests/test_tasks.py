import pytest
from users.models import User
from tasks.models import Task
from tasks.models import Category

@pytest.fixture
def user1(db):
    return User.objects.create_user('Adam Osiowy', 'addammmm@o2.pl', 'dsfgfgggf22234@$sa', id=1)

@pytest.fixture
def user2(db):
    return User.objects.create_user('Grzegorz Nowak', 'grzegorznowak12@gmail.com', '12345dsfeggggg')

@pytest.fixture
def category1(user1):
    return Category.objects.create(id=1, title="Default category", user_id=user1.id)

@pytest.mark.django_db
def test_category(category1):
    assert category1.title == "Default category"

@pytest.mark.django_db
def test_task(user1, category1):
    Task.objects.create(title="Spotkanie z przełożonym", priority="N", accepted=1, user_id=1)
    assert Task.objects.count() >= 1



@pytest.mark.django_db
def test_task2(user1, category1):
    Task.objects.create(title="Spotkanie z przełożonym", priority="N", accepted=1, user_id=1)
    Task.objects.create(title="Spotkanie z klientem", priority="N", accepted=1, user_id=1)
    Task.objects.create(title="Spotkanie z szefem", priority="N", accepted=1, user_id=1)
    Task.objects.create(title="Spotkanie z kierownikiem", priority="N", accepted=1, user_id=1)
    Task.objects.create(title="Spotkanie z promotorem", priority="W", accepted=1, user_id=1)
    assert Task.objects.count() >= 5


@pytest.fixture
def category2(user1):
    return Category.objects.create(id=2, title="High priority category", user_id=user1.id)
@pytest.fixture
def category3(user1):
    return Category.objects.create(id=3, title="Just another category", user_id=user1.id)


def test_task_categories(user1, category1,category2,category3):
    task1 = Task.objects.create(title="Spotkanie z przełożonym", priority="N", accepted=1, user_id=1, category_id=1)
    task2 = Task.objects.create(title="Spotkanie z klientem", priority="N", accepted=1, user_id=1, category_id=2)
    task3 = Task.objects.create(title="Spotkanie z szefem", priority="N", accepted=1, user_id=1, category_id=3)
    assert task1.category_id != task2.category_id and task2.category_id != task3.category_id




