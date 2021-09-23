from django.shortcuts import redirect, render, get_object_or_404
# from .models import Measurement
# from .forms import MeasurementModelForm
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

def location(request, lat, lon):
    """Shows a map with starting point of user, based on users location. Also shows the locations of tasks and their priorities.

    Args:
        request: request to return .html file
    Returns:
        .html file with a map of user starting point and places with task assigned to them

    """
    print(request.method)

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print(is_ajax)
    if is_ajax:
        if request.method == 'POST':
            print('1')
            print(lat)
            print(lon)
            data = json.load(request)
            n_lat = data.get('lat')
            n_lon = data.get('lon')
            if n_lat != lat or n_lon != lon:
                lat = n_lat
                lon = n_lon
                print('2')
                print(lat)
                print(lon)
                return redirect('location-2', n_lat, n_lon)
        else:
            return HttpResponse(json.dumps([{'lat':lat, 'lon':lon}]))

    print('lat:', lat)
    print('lon:', lon)

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
        'M': 'orange',
        'L': 'lightgray',
        'N': 'white'
    }

    for x in tasks:
        if x.l_lon and x.l_lat:
            folium.Marker([x.l_lat, x.l_lon], tooltip=x.title,
                    popup=x.localization,
                    icon=folium.Icon(color[x.priority], icon="cloud")).add_to(m)


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
    ip_ = get_ip_address(request)
    print(ip_)
    ip = '109.173.220.158'
    country, city, lat, lon = get_geo(ip)
    return redirect('location-2', lat, lon)


#def send_push(request):
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
    print('jest')
    return (str(a), nearest_task, str(round(y, 1)))

@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        data_tasks = how_many_tasks(user, float(data['head']), float(data['body']))
        print(data_tasks)
        if data_tasks[1] != None:
            payload = {'head': 'Zadań w okolicy: ' + data_tasks[0], 'body': 'Najbliższe zadanie: ' + data_tasks[1] + ' - ' +
                data_tasks[2] + 'km stąd'}
        else:
            payload = {'head': 'Brak zadań w okolicy'}
        print(payload)
        send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})

def home(request):
   webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
   vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
   user = request.user
   return render(request, 'location.html', {user: user, 'vapid_key': vapid_key})
