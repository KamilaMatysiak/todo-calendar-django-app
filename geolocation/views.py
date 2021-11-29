from django.shortcuts import redirect, render, get_object_or_404
# from .models import Measurement
# from .forms import MeasurementModelForm
from geoip2.errors import AddressNotFoundError
from geopy.geocoders import Nominatim
from .utils import get_geo, get_center_coordinates, get_zoom, get_ip_address
from geopy.distance import geodesic
import folium
from tasks.models import Task
from django.conf import settings
from django.conf.urls.static import static
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
import json
from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
def location(request, lat, lon):
    """Shows a map with starting point of user, based on users location. Also shows the locations of tasks and their priorities.

    Args:
        request: request to return .html file
    Returns:
        .html file with a map of user starting point and places with task assigned to them

    """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            n_lat = data.get('lat')
            n_lon = data.get('lon')
            if n_lat != lat or n_lon != lon:
                lat = n_lat
                lon = n_lon
                return redirect('location-2', n_lat, n_lon)
        else:
            return HttpResponse(json.dumps([{'lat': lat, 'lon': lon}]))

    m = folium.Map(width='100%', height='100%',
                   location=get_center_coordinates(lat, lon),
                   zoom_start=10)

    folium.Marker([lat, lon], tooltip='twoja lokalizacja',
                  popup="Twoja lokalizacja",
                  icon=folium.Icon('green')).add_to(m)

    # destination  marker
    tasks = (x for x in Task.objects.all() if x.user == request.user)

    color = {
        'H': 'red',
        'J': 'orange',
        'L': 'lightgray',
        'N': 'white'
    }

    for x in tasks:
        if x.l_lon and x.l_lat:
            html = x.localization + "\n" + '<p><a  href="/task-list/update_task/'+str(x.pk)+'">Przejdź do wybranego zadania</a></p>'
            iframe = folium.IFrame(html=html, width=200, height=200)
            popup = folium.Popup(iframe, max_width=2650)


            folium.Marker([x.l_lat, x.l_lon], tooltip=x.title,
                          popup=popup,
                          icon=folium.Icon(color[x.priority], icon="cloud")
                          ).add_to(m)

    m = m._repr_html_()
    # distance = None

    context = {
        'lat': lat,
        'lon': lon,
        'map': m,
    }

    t = loader.get_template('geolocation/location.html')
    return HttpResponse(t.render(context, request))


def start(request):
    try:
        ip = get_ip_address(request)
        country, city, lat, lon = get_geo(ip)
    except AddressNotFoundError:
        ip = '109.173.220.158'
        country, city, lat, lon = get_geo(ip)

    return redirect('location-2', lat, lon)


# def send_push(request):
#    payload = {"head": "Welcome!", "body": "Hello World"}
#    user = request.user
#    print(user)
#    send_user_notification(user=user, payload=payload, ttl=1000)

def how_many_tasks(user, lat, lon):
    a = 0
    y = 5
    nearest_task = None
    for x in Task.objects.all():
        if x.user == user and x.l_lat and x.l_lon:
            distance = geodesic((lat, lon), (x.l_lat, x.l_lon)).km
            if distance <= 5:
                a += 1
                if distance < y:
                    y = distance
                    nearest_task = x.title
    if not nearest_task:
        nearest_task = None
    return (str(a), nearest_task, str(round(y, 1)))
