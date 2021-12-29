import pytest_postgresql
import pytest
from pytest_postgresql import factories

postgresql_my_proc = factories.postgresql_proc(
    port=None, unixsocketdir='/var/run')
postgresql_my = factories.postgresql('postgresql_my_proc')


@pytest.mark.django_db
def test_example_postgres(postgresql):
    """Check main postgresql fixture."""
    cur = postgresql.cursor()
    cur.execute("INSERT INTO  users_userprofile VALUES ('kingus','1994-05-28','+48222222223',Null, Null, 123);")
    postgresql.commit()
    cur.close()
