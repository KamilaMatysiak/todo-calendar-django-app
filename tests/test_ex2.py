import pytest
from users.models import User


@pytest.mark.django_db
def test_my_user():
    me = User.objects.get(first_name='Adrian Charkiewicz')
    assert me.is_superuser

"""
@pytest.mark.django_db
def test_example_postgres(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO  users_userprofile VALUES ('kingus','1994-05-28','+48222222223',Null, Null, 123);")
    postgresql.commit()
    cur.close()
"""