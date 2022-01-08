from django.shortcuts import redirect, render, get_object_or_404
# from .models import Measurement
# from .forms import MeasurementModelForm
from geoip2.errors import AddressNotFoundError
from geopy.geocoders import Nominatim
from .utils import get_geo, get_center_coordinates, get_zoom, get_ip_address
from geopy.distance import geodesic
import folium
from tasks.models import Task
from calendar_app.models import Meeting
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
import re
from datetime import *


@xframe_options_exempt
def location(request, pk=None):
    """Shows a map with starting point of user, based on users location. Also shows the locations of tasks and their priorities.

    Args:
        request: request to return .html file
    Returns:
        .html file with a map of user starting point and places with task assigned to them

    """



    tasks = (x for x in Task.objects.all() if x.user == request.user)
    events = (x for x in Meeting.objects.all() if x.user == request.user)

    color = {
        'H': 'hue-rotate(150deg)',
        'J': 'saturate(0.9) sepia(0.07) brightness(1.5) contrast(3) hue-rotate(254deg)',
        'L': 'hue-rotate(270deg)',
        'N': 'grayscale(1) brightness(1.5)'
    }
    tasks_data =[]
    event_data = []
    for x in tasks:
        if x.l_lon and x.l_lat and not x.complete:
            path = "/task-list/" + str(x.id)
            html = f"<div><strong>{x.title}</strong> <br>{x.localization}<br>{x.date}<br><a style='color: #2F9CEB; width: 100%;' target='_blank' href='{path}'>Zobacz zadanie</a></div>"
            tasks_data.append([str(x.id), str(x.l_lat), str(x.l_lon), str(html), str(color[x.priority]), x.title])

    for x in events:
        if x.date_end > datetime.now().date():
            if x.l_lon and x.l_lat:
                path = "/calendar/day/" + re.sub(r"-", "/", str(x.date_start))
                html = f"<div><strong>{x.title}</strong> <br>{x.localization}<br>{x.date_start}<br><a style='color: #2F9CEB; width: 100%;' target='_blank' href='{path}'>Przejdź do kalendarza</a></div>"
                event_data.append([str(x.id), str(x.l_lat), str(x.l_lon), str(html), x.title])

    context = {
        'tasks': tasks,
        'tasks_data': tasks_data,
        'event_data': event_data
    }
    if pk is not None:
        context["marker_id"] = pk

    t = loader.get_template('geolocation/location.html')
    return HttpResponse(t.render(context, request))


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
