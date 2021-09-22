from django.shortcuts import render, get_object_or_404
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

def location(request):
    """Shows a map with starting point of user, based on users location. Also shows the locations of tasks and their priorities.

    Args:
        request: request to return .html file
    Returns:
        .html file with a map of user starting point and places with task assigned to them

    """
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user


    # distance = None
    # destination = None

    # nie odkomentowuj bo on psuje wszystko
    # obj = get_object_or_404(Measurement, id=1)
    # form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurements')
    ip_ = get_ip_address(request)
    print(ip_)
    ip = '109.173.220.158'
    country, city, lat, lon = get_geo(ip)
    location = geolocator.geocode(city)

    # koordynanty
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    # inicjowanie mapy
    m = folium.Map(width='100%', height='100%', location=get_center_coordinates(l_lat, l_lon), zoom_start=8)
    # znacznik lokalizacji początkowej
    folium.Marker([l_lat, l_lon], tooltip='twoja lokalizacja',
                  popup="kod pocztowy: " + city['postal_code'] + " miasto: " + city['city'],
                  icon=folium.Icon('green')).add_to(m)

    # if form.is_valid():
    # instance = form.save(commit=False)
    # destination_ = form.cleaned_data.get('destination')
    # destination = geolocator.geocode(destination_)

    # destination coordinates
    # d_lat = destination.latitude
    # d_lon = destination.longitude
    # pointB = (d_lat, d_lon)

    # distance calculation
    # distance = round(geodesic(pointA, pointB).km, 2)

    # initial folium map
    # m = folium.Map(width='100%', height='100%',
    #                 location=get_center_coordinates(lat, lon),
    #                 zoom_start=10)
    # ,
    # zoom_start=get_zoom(distance))
    # location marker

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            a_lat = data.get('lat')
            a_lon = data.get('lon')
            print(a_lat)
            print(a_lon)

            m = folium.Map(width='100%', height='100%',
                           location=get_center_coordinates(a_lat, a_lon),
                           zoom_start=10)

            folium.Marker([a_lat, a_lon], tooltip='twoja lokalizacja',
                          popup="TUTAJ JESTEŚ",
                          icon=folium.Icon('green')).add_to(m)

        # destination  marker
    tasks = (x for x in Task.objects.all() if x.user == request.user)

    color = {
        'H': 'red',
        'M': 'orange',
        'L': 'lightgray',
        'N': 'white'
    }
    count = 0
    for x in tasks:

        if x.l_lon and x.l_lat:
            folium.Marker([x.l_lat, x.l_lon], tooltip='cel podróży',
                          popup=x.localization,
                          icon=folium.Icon(color[x.priority], icon="cloud")).add_to(m)
        if(x.l_lat != None and x.l_lon != None):
            diff_lat = abs(float(x.l_lat) - float(lat))
            diff_lon = abs(float(x.l_lon) - float(lon))
            if(diff_lat < 0.01 or diff_lon < 0.01):
                count = count + 1
    if count > 0:
        print("Zadania w pobliżu: ", count)

        # draw the line between location and destination
        # line = folium.PolyLine(locations=[pointA, pointB], weight=2, color='blue')
        # m.add_child(line)

        # folium map modification
        # instance.location = location
        # instance.distance = distance
        # instance.save()

    m = m._repr_html_()
    # distance = None

    context = {
        # 'distance': distance,
        # 'destination': destination,
        # 'form': form,
        user: user,
        'vapid_key': vapid_key,
        'map': m,
    }

    print(vapid_key, user)

    return render(request, 'geolocation/location.html', context)


#def send_push(request):
#    payload = {"head": "Welcome!", "body": "Hello World"}
#    user = request.user
#    print(user)
#    send_user_notification(user=user, payload=payload, ttl=1000)

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
        payload = {'head': "Zadania w pobliżu:", 'body': "treść zadań?"}
        send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})

def home(request):
   webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
   vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
   user = request.user
   return render(request, 'location.html', {user: user, 'vapid_key': vapid_key})
