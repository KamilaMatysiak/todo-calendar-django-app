from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            UserModel.objects.create_superuser(username='admin',
                                               email='admin@v-todo.com',
                                               password='admin',  # change on genenv("ADMIN_PASSWORD")
                                               )
        except Exception as e:
            print("Got following exception: ", e)
