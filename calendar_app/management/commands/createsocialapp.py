from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            site = Site.objects.get_current()
            socialapp, _ = SocialApp.objects.get_or_create(
                provider='google',
                name='v-todo',
                # TODO: take from env
                client_id='228316449016-s0210ihiktgnnaifeej15m87blo7rb2d.apps.googleusercontent.com',
                secret='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',
            )
            print(socialapp)
            socialapp.sites.add(site)
            print(socialapp.__dict__)
            print('Created successfully')
        except Exception as e:
            print(e)
