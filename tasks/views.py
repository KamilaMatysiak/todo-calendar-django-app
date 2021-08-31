from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import datetime
from geopy.geocoders import Nominatim
from .utils import get_geo, get_center_coordinates, get_zoom, get_ip_address
from geopy.distance import geodesic
import folium


# Create your views here.

def homepage(request):
    return render(request, 'tasks/index.html')


@login_required
def task_list(request):
    tasks = (x for x in Task.objects.all() if x.user == request.user)
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
        return redirect('/')

    context = {"tasks": tasks, 'form': form}
    return render(request, 'tasks/task-list.html', context)


def index(request):
    return render(request, 'tasks/vtodo.html')


def addTask(request):
    tasks = Task.objects.all()
    form = TaskForm()
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.localization:
                geolocator = Nominatim(user_agent='measurements')
                destination_ = form.cleaned_data.get('localization')
                destination = geolocator.geocode(destination_)
                instance.l_lat = destination.latitude
                instance.l_lon = destination.longitude
            instance.user = request.user
            instance.save()
        return redirect('list')
        
    context = {"tasks": tasks, 'form': form}
    return render(request, 'tasks/add_task.html', context)


def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.localization:
                geolocator = Nominatim(user_agent='measurements')
                destination_ = form.cleaned_data.get('localization')
                destination = geolocator.geocode(destination_)
                instance.l_lat = destination.latitude
                instance.l_lon = destination.longitude
            instance.save()
            return redirect('list')

    context = {'form': form, 'id': pk}

    return render(request, 'tasks/update_task.html', context)


def deleteTask(request, pk):
    item = Task.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('list')

    context = {'item': item, 'id': pk}
    return render(request, 'tasks/delet.html', context)
