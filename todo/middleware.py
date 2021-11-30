from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.deprecation import MiddlewareMixin


class DynamicSiteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            current_site = Site.objects.get(domain=request.get_host())
        except Site.DoesNotExist:
            current_site = Site.objects.get(id=settings.SITE_ID)

        request.site = current_site
        settings.SITE_ID = current_site.id
        response = self.get_response(request)
        return response
